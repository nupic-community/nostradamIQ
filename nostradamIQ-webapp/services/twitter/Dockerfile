FROM redis:latest
RUN apt-get -y update && apt-get install -y python python-pip && apt-get -y upgrade
RUN pip install --upgrade pip
ADD * /twitter/
RUN pip install -r /twitter/requirements.txt
EXPOSE 8088
# CMD redis-server & cd /twitter && (python twitter_docker.py quake & python server.py & )
