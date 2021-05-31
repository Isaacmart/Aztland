#!/usr/bin/env python
import schedule
import time


def job(_text):
    _text.write("hello world \n")


text = open("listener.txt", "a")


schedule.every(10).second.do(job(text))


while True:
    schedule.run_pending()

