#!/bin/bash

assets=src/assets/data

mkdir $assets/patients
curl http://localhost:8080/fhir/Patient > $assets/Patients.json
for i in {1..8}; do curl http://localhost:8080/fhir/Patient/$i > $assets/patients/Patient-$i.json ; done

mkdir $assets/specimens
curl http://localhost:8080/fhir/Specimen > $assets/Specimens.json
for i in {1..8}; do curl http://localhost:8080/fhir/Specimen?subject=$i > $assets/specimens/Specimen-$i.json ; done

curl http://localhost:8080/fhir/Condition > $assets/Conditions.json

#mkdir $assets/molecularsequences
#for i in {3487,18077,19594,19596,20505,20717}; do curl http://localhost:8080/fhir/MolecularSequence/$i > $assets/molecularsequences/MolecularSequence-$i.json ; done
mkdir $assets/observations
for i in {3487,18077,19594,19596,20505,20717}; do curl http://localhost:8080/fhir/Observation?derived-from=$i > $assets/observations/Observation-$i.json ; done

for i in {3487,18077,19594,19596,20505,20717}
do 
	for p in {1..8} 
	do
		curl "http://localhost:8080/fhir/Observation?derived-from=$i&subject=$p" > $assets/observations/Observation-$i-$p.json
	done
done

