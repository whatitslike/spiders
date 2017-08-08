#!/bin/sh

# kill running tasks first
ps -ef | grep consumer | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep crawl | grep -v grep | awk '{print $2}' | xargs kill -9

PY_BIN='/home/pengfei/anaconda3/bin/python'

$PY_BIN start_consumer.py > /tmp/spider.log 2>&1 &
$PY_BIN start_consumer.py > /tmp/spider.log 2>&1 &
$PY_BIN start_consumer.py > /tmp/spider.log 2>&1 &
$PY_BIN start_consumer.py > /tmp/spider.log 2>&1 &
$PY_BIN start_consumer.py > /tmp/spider.log 2>&1 &
$PY_BIN start_crawl.py    > /tmp/spider.log 2>&1 &
