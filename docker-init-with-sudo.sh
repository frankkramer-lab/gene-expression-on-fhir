#!/bin/bash

echo "Start docker container:"

## Get sudo access
sudo -v

## run the official HAPI FHIR JPA server
## https://github.com/hapifhir/hapi-fhir-jpaserver-starter

## download the docker image
## (not really necessary)
echo "Load HAPI docker image..."
sudo docker pull hapiproject/hapi:latest

## run the image
echo "Run docker container..."
sudo docker run -dit \
	-p 8080:8080 \
	--name hapi-fhir-server \
	hapiproject/hapi:latest
	
## wait for the server to startup
echo "Wait 1m for the server to startup..."
sleep 1m

## configure the website
echo "Customize the website..."
sudo docker cp HAPI-FHIR-server/MISIT.png hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/img/
sudo docker cp HAPI-FHIR-server/tmpl-banner.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/
sudo docker cp HAPI-FHIR-server/tmpl-navbar-top-farright.html hapi-fhir-server:/usr/local/tomcat/webapps/ROOT/WEB-INF/templates/

## restart the container to activate the new template
echo "Restart the container to apply changes..."
sudo docker restart hapi-fhir-server

