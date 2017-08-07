#!/bin/bash

# kill running tasks first
ps -ef | grep consumer | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep crawl | grep -v grep | awk '{print $2}' | xargs kill -9

python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_consumer.py > /dev/null 2>&1 &
python start_crawl.py > /dev/null 2>&1 &
