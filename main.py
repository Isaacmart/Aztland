from flask import Flask, request, abort
from flup.server.fcgi import WSGIServer


app = Flask(__name__)


@app.route('/webhookListener.py')
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)


if __name__ == '__name__':
    WSGIServer(app(), bindAddress='/var/www/jdsdkf.xyz/html/CryptoTrader').run()


