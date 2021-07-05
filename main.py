from flask import Flask, request, abort, render_template
from open_position import OpenPosition
from order import Order
from get_indicators import GetAnyMACD
from cbpro.authenticated_client import AuthenticatedClient
from app_methods import *
import Data

app = Flask(__name__)

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order()
x = OpenPosition(order=new_order)


@app.route("/", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        print(request.get_json(force=True))
        return 'success!', 200
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        abort(400)






