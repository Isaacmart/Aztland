#!/usr/bin/env python3
import schedule


def job():
    print("hello world")


schedule.every(10).seconds.do(job)


while True:
    schedule.run_pending()

