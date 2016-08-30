#!/bin/bash

USER_PATTERN="loadtest"
PASSWORD_PATTERN="password_"
COUNT=$1

function curl_command {
  index=$1
  username=${USER_PATTERN}${index}
  password=${PASSWORD_PATTERN}${index}

  curl -siL -X POST \
    --data "username=${username}&password=${password}" \
    --cookie 'XSRF-TOKEN: blablabla' \
    --header 'X-Requested-With: XMLHttpRequest' \
    --header 'X-XSRF-TOKEN: blablabla' \
    http://localhost:3333/login |\
    grep '^HTTP'
}

for index in $(seq $COUNT); do
  curl_command $index &
  PIDS="$PIDS $!"
  sleep 1
done

wait $PIDS
