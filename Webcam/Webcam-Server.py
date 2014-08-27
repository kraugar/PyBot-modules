from flask import Flask, request
import base64
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

image64 = ""

@app.route('/image', methods = ["GET"])
def get_image():
        global image64
	return '<html><head><meta http-equiv="refresh" content=".05;"></head><body><img alt="Embedded Image" src="data:image/jpeg;base64,' + image64 + '" /></body></html>'

@app.route('/put', methods = ["GET"])
def post_image():
    global image64
    if request.method == "GET":
        image64 = request.args.get('image').replace("-","+").replace("_","/")
        
        return "DONE"

app.run(host='0.0.0.0')
