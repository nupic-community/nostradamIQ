FROM redis:latest
RUN apt-get -y update && apt-get install -y python python-pip
ADD * /twitter/
RUN pip install -r /twitter/requirements.txt
CMD redis-server & cd /twitter && (python twitter_docker.py quake & python server.py &)
