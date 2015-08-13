FROM redis:latest
RUN apt-get -y update && apt-get install -y python python-pip
RUN pip install tinydb requests redis
ADD https://github.com/nupic-community/nostradamIQ/tree/master/nostradamIQ-webapp/proxy/proxy.py /proxy/
COPY urls.txt /proxy/
CMD redis-server && cd /proxy && python proxy.py
