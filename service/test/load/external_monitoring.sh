#!/bin/bash

monitored=$1

if [ -z $2 ]
then
    output='/tmp/extra_monitoring'
else
    output=$2
fi


pid=$(pgrep -f "^$monitored")
echo `pgrep -f "cron"`
echo "$pid $monitored"

echo "Time Threads CPU Mem TCP/UDP" >> $output

time=0
while true; do
    threads=$(grep "Threads" /proc/$pid/status | cut -f2)

    cpu_mem=$(ps -p  $pid  -o \%cpu,\%mem | sed -n 2p)

    tcp_udp=$(sudo netstat -tuapen | grep $pid | wc -l)

    echo "$time $threads $cpu_mem $tcp_udp" >> $output

    sleep 2

    ((time=time+2))
done
