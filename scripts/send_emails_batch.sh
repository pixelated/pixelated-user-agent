#!/bin/bash

for i in `seq $1`; do
    echo Sending mail $i
    sendemail -f metrics@dev.pixelated-project.org -t metrics@dev.pixelated-project.org -u Hello$i -m Ha$i
done
