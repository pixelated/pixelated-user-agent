#!/bin/bash

how_many=$1
user_from=$2
user_to=$3

if [ -z $hostname ]
then
    hostname='unstable.pixelated-project.org'
fi

for user_count in `seq $2 $3`; do
    for i in `seq $1`; do
        echo Sending mail $i for user$user_count
        swaks -S -f ltest$user_count@$hostname -t ltest$user_count@$hostname -s localhost
    done
done
