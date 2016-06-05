#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Script responsible for simulating cloud.
"""
from cloud import Cloud
from time import sleep

def main():
    center = [-10, -17]
    radius = 5
    cloud_sim = Cloud(center,radius)
    
    while True:
        cloud_sim.check_mailbox()
        sleep(0.1)

if __name__ == "__main__":
    main()
