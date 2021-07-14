from flask import Flask, request, abort, render_template
from open_position import OpenPosition
from order import Order
from capital import Capital
from cbpro.authenticated_client import AuthenticatedClient
from indicators import *
from app_methods import *
import Data

app = Flask(__name__)

key = Data.API_Public_Key
b64secret = Data.API_Secret_Key
passphrase = Data.Passphrase


client = AuthenticatedClient(key, b64secret, passphrase)
new_order = Order()
position = OpenPosition(new_order)
funds = Capital(client)


@app.route("/", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        new_request = request.get_json(force=True)
        if float(new_request['hist']) >= 0 and float(new_request['volume']) >= float(new_request['volumema']):
            print(new_request['ticker'])
        return 'success', 200
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        abort(400)






