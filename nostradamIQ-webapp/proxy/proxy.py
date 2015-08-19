try:
    import urllib.parse as urlparse
except ImportError:
    # py2
    import urlparse

import tornado.httpclient
import tornado.web

import datetime
import redis
import base64

REDIS = redis.Redis()

CACHE_MIN = 5 # only for dev go for a dict with individual TTLs
# from chache_times import CACHE_MIN # Production
FILTER = False # To only accept urls in urls.txt

if FILTER == True:
    with open('urls.txt') as f:
        VALID_URLS = f.read().splitlines()
    f.close()

# headers to remove as of HTTP 1.1 RFC2616
# http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html
hop_by_hop_headers = set([
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade',
])


class ProxyHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kw):
        self.proxy_whitelist = kw.pop('proxy_whitelist', None)
        self.origin_whitelist = kw.pop('origin_whitelist', None)
        # Remove the '?'' Cesium prepends to the Proxy-Request:
        self.url = None
        try:
            print self.request.uri
            if '?' == self.request.uri[0]:
                self.request.uri = self.request.uri[1:]
        except:
            pass

        super(ProxyHandler, self).__init__(*args, **kw) #super(tornado.web.RequestHandler, self).__init__(*args, **kw)

    def check_proxy_host(self, url_parts):
        if self.proxy_whitelist is None:
            return

        url = '%s://%s' % (url_parts.scheme, url_parts.netloc)

        if url in self.proxy_whitelist or url == 'http://nostradamiq.org':
            return

        raise tornado.web.HTTPError(403)

    def check_origin(self):
        if self.origin_whitelist is None:
            return

        if 'Origin' not in self.request.headers:
            raise tornado.web.HTTPError(403)

        if self.request.headers['Origin'] not in self.origin_whitelist:
            raise tornado.web.HTTPError(403)

    def response_handler(self, response):
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            self.set_status(500)
            self.write('Internal server error:\n' + str(response.error))
            self.finish()
            return

        if response.code == 599:
            # connection closed
            self.set_status(502)
            self.write('Bad gateway:\n' + str(response.error))
            self.finish()
            return

        self.set_status(response.code)
        # copy all but hop-by-hop headers
        for header, v in response.headers.items():
            if header.lower() not in hop_by_hop_headers:
                self.set_header(header, v)

        origin = self.request.headers.get('Origin', '*')
        self.set_header('Access-Control-Allow-Origin', origin)

        if self.request.method == 'OPTIONS':
            if 'Access-Control-Request-Headers' in self.request.headers:
                # allow all requested headers
                self.set_header('Access-Control-Allow-Headers',
                    self.request.headers.get('Access-Control-Request-Headers', ''))

            self.set_header('Access-Control-Allow-Methods',
                response.headers.get('Allow', ''))

            if response.code == 405:
                # fake OPTIONS response when source doesn't support it
                # as OPTIONS is required for CORS preflight requests.
                # the 405 response should contain the supported methods
                # in the Allow header.
                self.set_status(200)
                self.clear_header('Content-Length')
                self.finish()
                return

        if response.body:
            # SAVE RESPONSE IN REDIS AND RETURN IT
            content = response.body
            content = base64.b64encode(content)
            type_content = response.headers.get('Content-Type', '')
            print "\nContent-Type: {0}".format(type_content)
            redis_obj = [type_content, content]
            # TODO: Write to file as well for long term storage
            REDIS.setex(self.url, redis_obj, CACHE_MIN*60) # CACHE_MIN[url]
            print "\nURL: {0} was inserted in REDIS-Cache with TTL: {1} minutes!\n".format(self.url, CACHE_MIN) # CACHE_MIN[url]
            self.write(response.body)
            self.finish()

    @tornado.web.asynchronous
    def request_handler(self, url):
        print url

        url_parts = urlparse.urlparse(url)
        # We are from your side ;)
        self.request.headers['Host'] = url_parts.netloc
        self.check_proxy_host(url_parts)
        self.check_origin()

        if self.request.query:
            url = url + '?' + self.request.query
        req = tornado.httpclient.HTTPRequest(
            url=url,
            method=self.request.method,
            body=self.request.body,
            headers=self.request.headers,
            follow_redirects=True, #False,
            allow_nonstandard_methods=True,
            use_gzip=False, # otherwise tornado will decode proxied data
        )

        # For saving it in Redis
        #self.url = url
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            redis_response = REDIS.get(self.url)
            if redis_response == None:
                # Have the AJAX Client fetch the content
                client.fetch(req, self.response_handler)
            else:
                # REDIS hold everything as a string, so get rid of all the stuff...
                redis_obj = redis_response[1:-1].split(',')
                type_content = redis_obj[0]
                content = redis_obj[1]
                # Get content from Redis and finish request
                self.set_header('Content-Type', type_content)
                content = base64.b64decode(content)
                print "\nGot Request handeled by Redis! TTL left: {0}".format(REDIS.ttl(self.url))
                self.write(content)
                self.finish()    

        except tornado.httpclient.HTTPError as e:
            # pass regular HTTP errors from server to client
            if hasattr(e, 'response') and e.response:
                self.response_handler(e.response)
            else:
                raise

    # alias HTTP methods to generic request handler
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS']
    get = request_handler
    post = request_handler
    put = request_handler
    delete = request_handler
    head = request_handler
    options = request_handler
