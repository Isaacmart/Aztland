from flask import Flask, request, abort
from flup.server.fcgi import WSGIServer


app = Flask(__name__)


@app.route('/webhook.py', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)


while True:
    WSGIServer(app).run()


