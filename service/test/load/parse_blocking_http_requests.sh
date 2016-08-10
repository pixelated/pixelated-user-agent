#!/bin/bash

operations=(start_authentication process_challenge fetch_attributes validated_get fetch_soledad_json fetch_smtp_json)

for op in ${operations[@]}; do
    value=$(grep $op /root/MetricsTime | cut -d' ' -f2- | sort -n | tail -1 | cut -d' ' -f1)
    echo $op: $value
done;
