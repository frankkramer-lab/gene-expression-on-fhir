#!/bin/bash
## run the official HAPI FHIR JPA server
## https://github.com/hapifhir/hapi-fhir-jpaserver-starter

## download the docker image
## (not really necessary)
docker pull hapiproject/hapi:latest

## run the image
docker run -dit \
	-p 8080:8080 \
	--name hapi-fhir-server \
	hapiproject/hapi:latest
	
## wait for the server to startup
sleep 1m

## configure the website
docker cp MISIT.png hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/img/
docker cp tmpl-banner.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/
docker cp tmpl-navbar-top-farright.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/

## restart the container to activate the new template
docker restart hapi-fhir-server

