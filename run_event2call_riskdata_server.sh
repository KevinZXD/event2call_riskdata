#!/bin/bash
start_server() {
    (nohup python3 event2call_riskdata_app.py >>server.log 2>&1 &)
}

FIRST_ARG=${1:-simple}
if [ $FIRST_ARG = "--with-watch-dog" ]; then
    TARGET_NUMBER=1
    while [ 1 ]; do
        DOG_NUMBER=$(ps -ef | grep "event2call_riskdata_app.py" | grep -v "grep" | wc -l)
        if [ $DOG_NUMBER -lt $TARGET_NUMBER ]; then
            echo "$(date +%Y-%m-%d\ %H:%M:%S) increase event2call_riskdata_app.py server number to $TARGET_NUMBER"
            start_server
            sleep 10
        else
            sleep 10
        fi
    done
else
    start_server
fi