#!/bin/bash

USER_PREFIX="loadtest"
PASSWORD_PREFIX="password_"

PROVIDER="dev.pixelated-project.org"
RUNS=9
USERS=1
SLEEP=1

function show_help {
    echo "Run several tests against login"
    echo
    echo " --user|-u - array with amount of tests split by comma"
    echo " --runs|-r - how many times a tests is going to run"
    echo " --provider|-p - set the provider"
    echo " --sleep|-s - time to sleep between requests"
    echo " --help|-h - show help message"
}

function run_on_vagrant {
    vagrant ssh -c "$@" > /dev/null 2>&1
}

function curl_login {
    index=$1
    username=${USER_PREFIX}${index}
    password=${PASSWORD_PREFIX}${index}

    curl -siLD - \
        -w "total time: %{time_total}\n" \
        -o /dev/null \
        -X POST \
        --data "username=${username}&password=${password}" \
        --cookie 'XSRF-TOKEN: blablabla' \
        --header 'X-Requested-With: XMLHttpRequest' \
        --header 'X-XSRF-TOKEN: blablabla' \
        http://localhost:3333/login |\
    tee -a load-test.log |\
    grep '^HTTP' |\
    sed 's/\(.*\)/      - \1/'
}

while [[ $# > 0 ]]; do
    case $1 in
        --users|-u)
            USERS=$2
            shift
        ;;
        --runs|-r)
            RUNS=$2
            shift
        ;;
        --provider|-p)
            PROVIDER=$2
            shift
        ;;
        --sleep|-s)
            SLEEP=$2
            shift
        ;;
        --help|-h)
            show_help
            exit 0
        ;;
    esac
    shift
done

run_on_vagrant "pkill pixelated"
run_on_vagrant "rm ~/MetricsTime"
run_on_vagrant "mkdir -p /vagrant/service/test/login/metrics"

for user in $(tr ',' ' ' <<< $USERS); do
    echo "> Run for $user user(s)"

    for run in $(seq $RUNS); do
        echo "  > Running $run of $RUNS runs"
        echo "  > Starting Pixelated UA"
        run_on_vagrant "nohup pixelated-user-agent --host 0.0.0.0 --multi-user --provider=$PROVIDER & sleep 1"
        until curl -s "http://localhost:3333" -o /dev/null 2>&1; do :; done

        for index in $(seq $user); do
            echo "    > Logging $USER_PREFIX$index"
            curl_login $index &
            PIDS="$PIDS $!"
            sleep $SLEEP
        done

        wait $PIDS
        PIDS=""
        echo "  > Killing Pixelated UA"
        run_on_vagrant "pkill pixelated"

        echo
    done
    run_on_vagrant "mv ~/MetricsTime /vagrant/service/test/login/metrics/${user}-users.txt"
    echo
done
