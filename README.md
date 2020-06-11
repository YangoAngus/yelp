# yelp cawler

*This is crawler for get data from*[https://yelp.com]
*System managed in docker-compose*
*Components: scrapy, mysql, phpmyadmin*
*Admin login - yelpdb, password - yelpdb, database user - yelpdb*
*You can will add proxies in proxy_list.txt in yelp_scrapy_container*
*This solution for proxy rotating* [https://pypi.org/project/scrapy-rotating-proxies/]
*This solution for user agents rotating* [https://github.com/cnu/scrapy-random-useragent]

## install docker
*install docker:* [https://docs.docker.com/get-docker/]
*install docker-compose:* [https://docs.docker.com/compose/install/]

## start in swarm mode
*Go to main project folder*
*Example of cli commands in ubuntu os*
```
$ cd yelp
```
*Make build*
```
$ docker-compose build
```
*init swarm*
```
$ docker stack init
```
*Run containers*
```
$ docker stack deploy -c docker-compose.yml yelp
```
*You can view statistic*
```
$ docker stats
```
*For remove stack*
```
$ docker stack rm yelp
``` 

 





