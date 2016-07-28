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

couchpid=$(pgrep -f "beam.smp")

echo "Time Date Threads CPU Mem CouchCPU CouchMem TCP/UDP Entropy" >> $output

time=0
while true; do
    threads=$(grep "Threads" /proc/$pid/status | cut -f2)
    entropy=$(cat /proc/sys/kernel/random/entropy_avail)
    cpu_mem=$(ps -p  $pid  -o \%cpu,\%mem | sed -n 2p)

    tcp_udp=$(sudo netstat -tuapen | grep $pid | wc -l)

    date=$(date +'%Y-%m-%d %H:%M:%S.%5N')

    couch_cpu_mem=$(ps -p  $couchpid  -o \%cpu,\%mem | sed -n 2p)

    echo "$time $date $threads $cpu_mem $couch_cpu_mem $tcp_udp $entropy" >> $output

    sleep 2

    ((time=time+2))
done
