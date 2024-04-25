#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
pip3 install aiokafka
python3 /Users/blacktiger/PycharmProjects/fluent/kafka/producer.py