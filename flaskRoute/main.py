from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def add():
    data = request.json
    data_from_handler = requests.post("url", json=data) #Вместо url пишите url обработчика
    return jsonify({'result': data_from_handler.json()})


if __name__ == "__main__":
    app.run()
