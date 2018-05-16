batoru-royale
=============

[![Build Status](https://travis-ci.org/Ishino/batoru-royale.svg?branch=master)](https://travis-ci.org/Ishino/batoru-royale)
[![Gitter](https://badges.gitter.im/Ishino/batoru-royale.svg)](https://gitter.im/Ishino/batoru-royale)
[![Dependency Status](https://www.versioneye.com/user/projects/56a653c51b78fd0035000171/badge.svg?style=flat-square)](https://www.versioneye.com/user/projects/56a653c51b78fd0035000171)

Heroku URL: https://intense-anchorage-9323.herokuapp.com

Code coverage report: http://ishino.github.io/batoru-royale/cover/index.html

Learning Python the fun way.

## prerequisites ##

- Python 3.x


## Kibana ##

You can use Kibana to visualize the charater creation and fight statistics. In the kibana folder are JSON exports
to use in Kibana 4.3

To use all the saved objects add the following indices:

- creation
- fights

To the fights filter, add a scripted field

name: level_difference
script: doc['fighter_level'].value - doc['opponent_level'].value

## Docker ##

Build the images

- docker pull redis
- docker pull rabbitmq
- docker pull elasticsearch

- docker build -t batoru-royale .

Run the services

- docker-compose up -d

Manually:

- docker run --name batoru-redis -d -P -p 6379:6379 redis
- docker run --name batoru-rabbitmq -d -P -p 5672:5672 rabbitmq
- docker run --name batoru-elasticsearch -d -P -p 9200:9200 elasticsearch

- docker run --name batoru-royale-socket --link batoru-redis:redis --link batoru-rabbitmq:rabbitmq --link batoru-elasticsearch:elasticsearch -p 5000:5000 -d -P batoru-royale python batoru_socket.py
- docker run --name batoru-royale-read --link batoru-redis:redis --link batoru-rabbitmq:rabbitmq --link batoru-elasticsearch:elasticsearch -d batoru-royale python read.py
