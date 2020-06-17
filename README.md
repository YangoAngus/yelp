# yelp cawler

*This is crawler for get data from*[https://yelp.com]
*system managed in docker-compose*
*components: scrapy, mysql, phpmyadmin*
*admin login - yelpdb, password - yelpdb, database user - yelpdb*
*you can will add proxies in proxy_list.txt in yelp_scrapy_container*
*this solution for proxy rotating* [https://pypi.org/project/scrapy-rotating-proxies/]
*this solution for user agents rotating* [https://github.com/cnu/scrapy-random-useragent]

## install docker
*install docker:* [https://docs.docker.com/get-docker/]
*install docker-compose:* [https://docs.docker.com/compose/install/]

## start in swarm mode
*Go to main project folder,*
*example of cli commands in ubuntu os*
```
$ cd yelp
```
*Make build*
```
$ docker-compose build
```
*Init swarm*
```
$ docker swarm init
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

 





