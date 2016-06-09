#!/usr/bin/env bash
mkdir -p /tmp/sst
rm /tmp/sst/*;

for i in $(seq 0 $(($1 - 1))); do
	python3 robot.py env.conf $i &
done
python3 cloud.py env.conf
