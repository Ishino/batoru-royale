#!/usr/bin/env bash

docker run --name batoru-redis -d -P -p 6379:6379 redis
docker run --name batoru-rabbitmq -d -P -p 5672:5672 rabbitmq
docker run --name batoru-elasticsearch -d -P -p 9200:9200 elasticsearch

docker run --name batoru-royale-socket --link batoru-redis:redis --link batoru-rabbitmq:rabbitmq --link batoru-elasticsearch:elasticsearch -p 5000:5000 -d -P batoru-royale python batoru_socket.py
docker run --name batoru-royale-read --link batoru-redis:redis --link batoru-rabbitmq:rabbitmq --link batoru-elasticsearch:elasticsearch -d batoru-royale python read.py
