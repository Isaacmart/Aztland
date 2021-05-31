#!/usr/bin/env python
import schedule
import time


def job():
    print("hello world")


schedule.every(10).second.do(job)

while True:
    schedule.run_pending()

