from threading import Thread
from threading import Lock
import os
import sys
import psutil

process = psutil.Process(os.getpid())
print(process.memory_info())  # in bytes


