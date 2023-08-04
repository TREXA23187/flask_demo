from flask import Flask, render_template, request
from model.enter import run
import json
import requests
import base64
import pickle
import pandas as pd

app = Flask(__name__)

localhost = "host.docker.internal"
# localhost = "localhost"
# localhost = "47.243.60.114"

with open('config.json', 'r', encoding='utf-8') as fp:
    config = json.load(fp)

if config["type"] == "training":
    try:
        model_evaluation = run(config)

        with open('./model/model.pickle', 'rb') as f:
            model_file = f.read()

        model_file_base64 = base64.b64encode(model_file).decode()
        response = requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                                 json={"task_id": config["taskId"], "operation": "success",
                                       "model_file": model_file_base64})
    except Exception as e:
        print(e)
        response = requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                                 json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    if config["type"] == "training":
        return render_template("index.html", config=config, model_evaluation=model_evaluation)


@app.route('/predict', methods=['POST'])
def predict():
    # if config["type"] == "deployment":
    if config["type"] == "training":
        with open("model/model.pickle", 'rb') as pickle_file:
            model = pickle.load(pickle_file)

        data = request.get_json()
        print(data)

        new_data = pd.DataFrame({
            'SepalLengthCm': [5.1, 6.2],
            'SepalWidthCm': [3.5, 3.4],
            'PetalLengthCm': [1.4, 5.4],
            'PetalWidthCm': [0.2, 2.3]
        })

        predictions = model.predict(new_data)

        return list(predictions)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
