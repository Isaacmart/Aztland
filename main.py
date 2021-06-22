from flask import Flask, request, abort, render_template
from open_position import OpenPosition
from open_authenticated import Order
from get_indicators import GetAnyMACD
from cbpro.authenticated_client import AuthenticatedClient
from webhookListener import get_time
import Data

app = Flask(__name__)

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase

x = OpenPosition()
y = GetAnyMACD()
v = Order()
client = AuthenticatedClient(key, b64secret, passphrase)
r = get_time(0)


@app.route("/", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        print(request.get_json(force=True))
        return 'success!', 200
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        abort(400)





