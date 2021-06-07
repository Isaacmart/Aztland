#!/usr/bin/python3.7
import sys
activate_this = '/var/www/jdsdkf.xyz/html/CryptoTrader/env/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, '/var/www/jdsdkf.xyz/html/CryptoTrader')
from main import application as application