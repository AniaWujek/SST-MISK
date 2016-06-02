#!/usr/bin/env bash
mkdir -p /tmp/sst
for f in $(ls /tmp/sst); do
	rm /tmp/sst/$f;
done;

for i in $(seq 0 $(($1 - 1))); do
	python3 robot.py env.conf $i &
done
