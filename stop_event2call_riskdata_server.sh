#!/bin/bash
ps -ef|grep "event2call_riskdata"|grep -v "grep"|awk '{print $2}'|xargs kill -9