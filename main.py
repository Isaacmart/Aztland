from flask import Flask, request, abort
from webhookListener import write_to_csv


app = Flask(__name__)


@app.route("/", methods=["POST"])
def application():
    if request.method == 'POST':
        write_to_csv(request.json)
        print(request.json)
        return 'success!', 200
    else:
        abort(400)




