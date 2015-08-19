from __future__ import print_function

import re
import sys

import tornado.ioloop
import tornado.web
import tornado.log

from proxy import ProxyHandler


def run_proxy(bind, app_path=None, debug=False,
    proxy_whitelist=None, origin_whitelist=None):
    handler = [
        (r'/proxy/(.*)', ProxyHandler, { #r'/proxy/[?](.*)' # ^/proxy/[?](.*) TODO Should work!
            'proxy_whitelist': proxy_whitelist,
            'origin_whitelist': origin_whitelist,
            }
        ),
    ]
    if app_path:
        handler.append(
            (r'/app/(.*)', tornado.web.StaticFileHandler, {'path': app_path})
        )
    app = tornado.web.Application(handler, debug=debug)
    app.listen(bind[1], bind[0])
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

def parse_bind_address(address, default=('localhost', 8080)):
    """
    >>> parse_bind_address('80')
    ('localhost', 80)
    >>> parse_bind_address('0.0.0.0')
    ('0.0.0.0', 8080)
    >>> parse_bind_address('0.0.0.0:8081')
    ('0.0.0.0', 8081)
    """
    if ':' in address:
        host, port = address.split(':', 1)
        port = int(port)
    elif re.match('^\d+$', address):
        host = default[0]
        port = int(address)
    else:
        host = address
        port = default[1]
    return host, port


def main():
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('--app-dir')
    parser.add_option('-b', '--bind', default='localhost:8888')
    parser.add_option('--allow-proxy', default=None)
    parser.add_option('--allow-origin', default='SELF')
    parser.add_option('--debug', default=False, action='store_true')

    options, args = parser.parse_args()

    host, port = parse_bind_address(options.bind)

    tornado.log.enable_pretty_logging()

    print("Starting CORS-Proxy...", file=sys.stderr)
    print("CORS proxy at http://%s:%d/proxy/" % (host, port), file=sys.stderr)

    if options.app_dir:
        print("Hosting %s at http://%s:%d/app/" % (options.app_dir, host, port),
            file=sys.stderr)

    proxy_whitelist = []
    if options.allow_proxy:
        proxy_whitelist = set(options.allow_proxy.split(','))
        if 'ALL' in proxy_whitelist:
            proxy_whitelist = None

    origin_whitelist = []
    if options.allow_origin:
        origin_whitelist = set(options.allow_origin.split(','))
        if 'SELF' in origin_whitelist:
            origin_whitelist.remove('SELF')
            origin_whitelist.add('http://%s:%d' % (host, port))
        if 'ALL' in origin_whitelist:
            origin_whitelist = None

    try:
        run_proxy((host, port), options.app_dir,
            debug=options.debug,
            proxy_whitelist=proxy_whitelist,
            origin_whitelist=origin_whitelist,
        )
    except KeyboardInterrupt:
        print("Exiting", file=sys.stderr)


if __name__ == '__main__':
    main()