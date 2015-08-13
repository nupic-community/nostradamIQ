FROM redis:latest
RUN apt-get -y update && apt-get install -y python python-pip
RUN pip install tinydb requests redis
ADD https://gist.githubusercontent.com/pajowu/019f6a83aaa22d3b4885/raw/proxy.py /proxy/
COPY urls.txt /proxy/
CMD redis-server & cd /proxy && python proxy.py
