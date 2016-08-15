#!/bin/bash

user="ltest"
password="password_"

while [[ $# -gt 1 ]];do
    arg="$1"
    case $arg in
        -c|--clients)
        number="$2"
        shift
        ;;
        -s|--sleep)
        sleep_time="$2"
        shift
        ;;
        -l|--start)
        start="$2"
        shift
        ;;
        -h|--host)
        host="$2"
        shift
        ;;
    esac
    shift
done

echo "number of clients: $number"
echo "sleep time in between launch: $sleep_time seconds"
echo "user number starts at $start"

((end=start+number))

if [ -z $host ]
then
    host='https://unstable.pixelated-project.org:8080/login'
fi

echo "host: $host"

for i in `seq $start $end`; do
    time curl -sS -k -X POST -F "username=$user$i" -F"password=$password$i" $host &
    sleep $sleep_time
done


