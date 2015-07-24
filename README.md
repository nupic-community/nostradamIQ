# nostradamIQ - sensing our worlds disasters.
## Modern tech & principles of our brain -> intuitive & intelligent tool for nostradamIQ prediction

[![Join the chat at https://gitter.im/nupic-community/nostradamIQ](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/nupic-community/nostradamIQ?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# THIS IS WORK IN PROGRESS! DO NOT JUDGE, BUT FEEL FREE TO HELP/SHARE etc. ;)



## Requirements

- [NuPIC](https://github.com/numenta/nupic)
- [Redis](http://redis.io/) running locally
- Python, and [dependencies](requirements.txt)
- [Google Maps Javascript API Key](https://developers.google.com/maps/documentation/javascript/tutorial#api_key)
- Possibly: 
- [Cerebro2](https://github.com/numenta/nupic.cerebro2)
- [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)

## Usage

Include your API-Keys in webapp/API_KEYS.py (MAPS_API_KEY=< your API_KEY>)

- Start redis

  ```bash
  $ redis-server
  ```

- Start `run.py`

  ```bash
  $ python run.py
  ```

- Start webapp

  ```bash
  $ cd webapp
  $ python serve.py
  ```

- Open [http://localhost:8080](http://localhost:8080) in browser

## Usage via VM:

Include your API-Keys in webapp/API_KEYS.py (MAPS_API_KEY=< your API_KEY>) 
Download and install Docker client, Virtualbox, and Vagrant, and then:

```
source env.sh
vagrant up
docker build -t nostradamIQ .
docker run --name nostradamIQ-redis -d -p 0.0.0.0:6379:6379 redis
docker run \
  --name nostradamIQ-server \
  --link nostradamIQ-redis:broker \
  -e REDIS_HOST=broker \
  -d \
  -p 0.0.0.0:8080:8080 \
  -w /opt/numenta/nostradamIQ/webapp \
  nostradamIQ \
  python serve.py
docker run \
  --link nostradamIQ-redis:broker \
  -e REDIS_HOST=broker \
  nostradamIQ \
  python run.py
```

Redis, the nostradamIQ web service, and the nostradamIQ entry point are now running
in separate containers in a vm.  You should be able to access the web service
in a browser at [http://localhost:8080](http://localhost:8080)

_______________________________________________________________________________________________________________________________

Thanks to the NuPIC-Community, Austin, Lab75 and many more for help!

This is part of a [TEDx-Project](http://datanauts.tedxrheinmain.de/contest-submissions/natural-catashtrophies-prediction-system/); [their Bolg about this](http://datanauts.tedxrheinmain.de/blog/meanwhile-in-datanauts-country/).

See the Pitch!
[![here: www.youtube.com/watch?v=5eXk9V57-I0](http://img.youtube.com/vi/5eXk9V57-I0/0.jpg)](http://www.youtube.com/watch?v=5eXk9V57-I0)

The idea is to make the world a safe place by making nostradamIQ-prediction more efficient.
This will also lead to a nice tool for visualizing all kinds of natural phenomena, easily searchable with a timescale and choosable info-layers. The core-feature, though, is going to be a layer showing the probability for natural disasters determined by learning time and location based sequences and utilizing other tools like detecting anomal abnormal behavior, preassure and temperature anomalies and (hopefully) combining all to one useful and accurate prediction tool to help local governments and organisations to focus research and prepare for possible nostradamIQs.

### Let's use the technology of today and data from the past to make a better future for all!

"There are only patterns, patterns on top of patterns, patterns that affect other patterns. Patterns hidden by patterns. Patterns within patterns. 
If you watch close, history does nothing but repeat itself." 
-Someone smart 
