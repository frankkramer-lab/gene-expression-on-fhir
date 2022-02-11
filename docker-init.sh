#!/bin/bash

echo "Start docker container:"

## run the official HAPI FHIR JPA server
## https://github.com/hapifhir/hapi-fhir-jpaserver-starter

## download the docker image
## (not really necessary)
echo "Load HAPI docker image..."
docker pull hapiproject/hapi:latest

## run the image
echo "Run docker container..."
docker run -dit \
	-p 8080:8080 \
	--name hapi-fhir-server \
	hapiproject/hapi:latest
	
## wait for the server to startup
echo "Wait 1m for the server to startup..."
sleep 1m

## configure the website
echo "Customize the website..."
docker cp HAPI-FHIR-server/MISIT.png hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/img/
docker cp HAPI-FHIR-server/tmpl-banner.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/
docker cp HAPI-FHIR-server/tmpl-navbar-top-farright.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/

## restart the container to activate the new template
echo "Restart the container to apply changes..."
docker restart hapi-fhir-server

