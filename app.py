import json
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING
import certifi

with open('config.json', 'r') as f:
    config = json.load(f)

mongo_srv = config["MONGO_SRV"]
ca = certifi.where()
client = MongoClient(mongo_srv, tlsCAFile=ca)
db = client.rgorithm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/top50', methods=['GET'])
def get_top50():
    result_list = []
    for i in range(1, 51):
        result = list(db.songs.find({'rank': i}, {'_id': False}).sort('date', DESCENDING).limit(1))
        result_list.append(result)

    return jsonify({'title': 'top50 차트곡', 'info': result_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)