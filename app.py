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
        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "success",
                            "model_file": model_file_base64})
    except Exception as e:
        print(e)
        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    if config["type"] == "training":
        return render_template("index.html", config=config, model_evaluation=model_evaluation)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if config["type"] == "deployment":
            with open("model/model.pickle", 'rb') as pickle_file:
                model = pickle.load(pickle_file)

            feature_data = request.get_json()
            for key in feature_data.keys():
                feature_data[key] = [feature_data[key]]

            predictions = model.predict(pd.DataFrame(feature_data))

            requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                          json={"task_id": config["taskId"], "operation": "success"})

            return list(predictions)
    except Exception as e:
        print(e)
        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "fail"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
