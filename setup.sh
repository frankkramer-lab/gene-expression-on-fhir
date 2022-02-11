#!/bin/bash
 
echo "Setup FHIR genomics project:"

./data-download.sh

./docker-init.sh
echo "Wait 1m for the server to startup..."
sleep 1m

./fhir-upload.sh

./docker-httpd.sh
