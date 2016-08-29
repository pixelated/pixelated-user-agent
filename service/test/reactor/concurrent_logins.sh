#!/bin/bash

USER_PATTERN="loadtest"
PASSWORD_PATTERN="password_"
COUNT=$1

function curl_command {
  index=$1
  username=$USER_PATTERN$index
  password=$PASSWORD_PATTERN$index
  curl -sIL -X POST \
    --data "username=$username&password=$password" \
    --cookie 'XSRF-TOKEN: blablabla' \
    --header 'X-Requested-With: XMLHttpRequest' \
    --header 'X-XSRF-TOKEN: blablabla' \
    http://localhost:3333/login |\
    grep 'HTTP' |\
    tail -1
}

for index in $(seq $COUNT); do
  curl_command $index &
  sleep 1
done
wait
