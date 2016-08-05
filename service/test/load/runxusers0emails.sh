#!/bin/bash

REQUESTS=$(($1 * 100))

LEAP_PROVIDER=dev.pixelated-project.org locust \
    -f /vagrant/service/test/load/login_and_browse.py \
    --no-web --num-request=$REQUESTS \
    --clients=$1  --hatch-rate=1 --host=http://localhost:3333
mv ~/MetricsTime /vagrant/service/test/load/metrics/xusers0emails/${1}users-0emails.txt
