#!/bin/bash
for user in `seq $1`; do
	echo "Sending $2 mails for user loadtest$1"
	for email in `seq $2`; do
	    sendemail -f loadtest${user}@dev.pixelated-project.org -t loadtest${user}@dev.pixelated-project.org -u Hello$email -m Ha$email
	done
done
