#!/usr/bin/env bash

for i in $(seq 0 $1); do
	python3 robot.py env.conf $i &
done
