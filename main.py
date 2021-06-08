from flask import Flask, request, abort
import csv
#from flup.server.fcgi import WSGIServer


app = Flask(__name__)



@app.route("/", methods=["POST"])
def application():
    if request.method == 'POST':
        to_write = open('webhook_log.csv', 'a')
        writer = csv.writer(to_write)
        writer.writerow(request.json + "\n")
        to_write.close()
        print(request.json)
        return 'success!', 200, request.json
    else:
        abort(400)




