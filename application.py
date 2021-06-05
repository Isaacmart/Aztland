from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def Listener():
    print(request.data)
    print(request.json)
    print(request.get_json(force=True))
