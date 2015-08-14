FROM redis:latest
RUN apt-get -y update && apt-get install -y python python-pip
RUN pip install -r requirements.txt
ADD * /twitter/
CMD redis-server & cd /twitter && (python twitter_docker.py quake & python server.py &)
