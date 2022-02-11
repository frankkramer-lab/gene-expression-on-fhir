#!/bin/bash

for i in {3487,18077,19594,19596,20505,20717}
do
  for p in {1..8} 
  do
    echo Observation-$i-$p.json
    curl "http://localhost:8080/fhir/Observation?derived-from=$i&subject=$p" > Observation-$i-$p.json
  done
done

