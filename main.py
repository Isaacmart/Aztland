from flask import Flask, request, abort
#from flup.server.fcgi import WSGIServer


app = Flask(__name__)

to_write = open("webhooks_log.txt", "a")


@app.route('/', methods=["POST"])
def application():
    if request.method == 'POST':
        print(request.json)
        to_write.write(request.json + "\n")
        return 'success!', 200
    else:
        abort(400)


#if __name__ == '__name__':
#    WSGIServer(app(), bindAddress='/var/www/jdsdkf.xyz/html/CryptoTrader').run()


