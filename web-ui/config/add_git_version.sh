#!/usr/bin/env bash

TEMPLATE_FILE="app/js/generated/hbs/templates.js"

COMMITISH=$(git rev-parse --short HEAD)
COMMITDATE=$(git show -s --format=%cr)

perl -pi -e "s/UNKNOWN_VERSION/$COMMITISH/" $TEMPLATE_FILE
perl -pi -e "s/COMMIT_DATE/$COMMITDATE/" $TEMPLATE_FILE

if [ ! -f "$TEMPLATE_FILE" ] ; then
    echo "file $TEMPLATE_FILE not found" 1>&2
    exit 1
fi

exit 0
