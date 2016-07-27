#!/bin/bash

REQUESTS=$(($1 * 20))

for i in `seq 9`; do 
    LEAP_PROVIDER=dev.pixelated-project.org locust \
        -f /vagrant/service/test/load/login_and_browse.py \
        --no-web --num-request=$REQUESTS \
        --clients=$1  --hatch-rate=1 --host=http://localhost:3333
    cp ~/MetricsTime /vagrant/service/test/metrics/${1}users-${2}emails-${i}.txt
    rm ~/MetricsTime
done
