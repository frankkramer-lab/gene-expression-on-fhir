#!/bin/bash

echo "Start docker container:"

## run the website within an apache server

## download the docker image
## (not really necessary)
echo "Load httpd docker image..."
docker pull httpd:2.4

## run the image
echo "Run docker container..."
docker run -dit \
	-p 8081:80 \
	--name ge-on-fhir-http \
	httpd:2.4
	
## configure the website
echo "Copy the website..."
docker cp web-app/dist/GEonFHIRlocal/. ge-on-fhir-http:/usr/local/apache2/htdocs/


