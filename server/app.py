from flask import Flask, abort, jsonify, send_file, request
from server import Server
from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)

@app.route("/claiming")
def getState():
    return str(Server.claiming).lower()

@app.route("/claim")
def claimImage():
    try:
        return send_file(Server.claimImage())
    except Exception as e:
        return jsonify(error = str(e), time = datetime.datetime.now().isoformat()), 400


@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify(error = "file is missing", time = datetime.datetime.now().isoformat()), 400
    try:
        size = Server.uploadImage(request.files['file'])
        return jsonify(size = size, time = datetime.datetime.now().isoformat())
    except Exception as e:
        return jsonify(error = str(e), time = datetime.datetime.now().isoformat()), 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)