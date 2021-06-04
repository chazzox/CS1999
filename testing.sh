#!/bin/bash


URL='127.0.0.1:5000'

echo "Testing Script"
echo "This file will test api reuqest to the server, it will consider a request a 'success' if it returns the expected status code"

echo 'Testing a post request with nothing in (Expecting code 400)'
DATA=$(curl -si -X POST "$URL/new" | grep 'HTTP/1.0')
if [[ $DATA =~ "400" ]];  then
    echo "$DATA - TEST PASSED MOVING ON."
else
    echo "TEST FAILED, PLEASE FIX."
fi

echo 'Testing a post request with missing keys (Expecting code 400)'
DATA=$(curl -si -X POST -d 'qty_wheels=4&algo=steady&flag_pattern=plain&qty_tyres=6' "$URL/new" | grep 'HTTP/1.0')
if [[ $DATA =~ "400" ]];  then
    echo "$DATA - TEST PASSED MOVING ON."
else
    echo "TEST FAILED, PLEASE FIX."
fi


echo 'Testing a post request with invalid data (Expecting code 400)'
DATA=$(curl -si -X POST -d 'qty_wheels=foo&power_type=bar&power_units=green&aux_power_type=some&aux_power_units=0&hamster_booster=0&flag_color=#000000&flag_pattern=plain&flag_color_secondary=#000000&tyres=knobbly&qty_tyres=4&armour=None&attack=None&qty_attacks=0&fireproof=0&insulated=0&antibiotic=test&banging=0&algo=offensive' "$URL/new" | grep 'HTTP/1.0')
if [[ $DATA =~ "400" ]];  then
	echo "$DATA - TEST PASSED MOVING ON."
else
    echo "TEST FAILED, PLEASE FIX."
fi

echo 'Testing a post request with valid data (Expecting code 200)'
DATA=$(curl -si -X POST -d 'qty_wheels=4&power_type=petrol&power_units=1&aux_power_type=None&aux_power_units=0&hamster_booster=0&flag_color=#000000&flag_pattern=plain&flag_color_secondary=#000000&tyres=knobbly&qty_tyres=4&armour=None&attack=None&qty_attacks=0&fireproof=0&insulated=0&antibiotic=0&banging=0&algo=offensive' "$URL/new" | grep 'HTTP/1.0')
if [[ $DATA =~ "200" ]];  then
    echo "$DATA - TEST PASSED MOVING ON."
else
    echo "TEST FAILED, PLEASE FIX."
fi



read -n 1 -r -s -p $'Press enter to exit script...\n'



