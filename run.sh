#!/bin/bash

# kill running tasks first
kill `ps -ef | grep consumer | grep -v grep | awk '{print $2}'`
kill `ps -ef | grep crawl | grep -v grep | awk '{print $2}'`

python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_crawl.py > /dev/null 2>&1 &
