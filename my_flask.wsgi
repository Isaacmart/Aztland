#!./env
import sys

activate_this = './env/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, './src')

from main import app as application