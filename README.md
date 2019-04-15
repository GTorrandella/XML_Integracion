# XML Integracion

>Thanks taking your time in finding TweetMaster!
>
>This project was created to learn Docker, Travis, Redis and XML during a college course.
>
>Autor: Gabriel Torrandella
>
>Professor: Juan Lagostena

## Introduction

_XML Integracion_ is a "bank's database simulator". It allows the saving and querring of the bank's clients and account information.

Is a command line aplication running inside two containers.

## Set Up

### Requierements

As a Docker aplication, you 'll only need Docker to be able to run this.

### Create a Docker Network

Because the app lives on two containers, it is necesary them share a network. Anyone will sufice.
To create a Docker Network, run:
```
docker network create integracionNet
```

### Set Up the database

Download the latest Redis image.
```
docker image pull redis
```
Then start the container.
```
docker container run -d --network integracionNet --name integracionRedis redis redis-server --appendonly yes
```
**NOTE** The container name **must** be _xmlredis_. Otherwise, the other half will not find the database.

### Set Up the command line app

Build the image.
```
docker image build -t integracion .
```

## Execution

### Using the app

Run the container as interactive in the same network as Redis.
```
docker container run -it --network integracionNet integracion
```

### Stoping the app

Stop the Redis' container.
```
docker container stop integracionRedis
```
And exit the app.

### Restarting the app

To resume operation in the same database, start the Redis' container.
```
docker container start integracionRedis
```
Then execute the command line app as normal.

### Data persistense

The information in the database will live between sesions while the Redis' container is not deleted.

## Missing features

 * Being able to download the images from DockerHub/DockerStore.
 * Some test cases.
