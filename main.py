from flask import Flask, request, abort
#from flup.server.fcgi import WSGIServer


app = Flask(__name__)

#to_write = open("webhooks_log.txt", "a")


@app.route("/", methods=["POST"])
def application():
    if request.method == 'POST':
        print(request.json)
        #to_write.write(request.json + "\n")
        return 'success!', 200, request.json
    else:
        abort(400)




