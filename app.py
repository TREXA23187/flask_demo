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

model_evaluation = None
if config["type"] == "training":
    try:
        model_evaluation = run(config)

        with open('./model/model.pickle', 'rb') as f:
            model_file = f.read()

        with open('./model/label_int_tag.json', 'rb') as f:
            label_int_tag = json.load(f)

        model_file_base64 = base64.b64encode(model_file).decode()
        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "success",
                            "model_file": model_file_base64, "label_int_tag": json.dumps(label_int_tag)})
    except Exception as e:
        print("error: ", e)
        model_evaluation = {}
        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    if config["type"] == "training":
        return render_template("index.html", config=config, model_evaluation=model_evaluation)


@app.route('/predict', methods=['POST'])
def predict():
    # try:
    if config["type"] == "deployment":
        with open("model/model.pickle", 'rb') as pickle_file:
            model = pickle.load(pickle_file)

        feature_data = request.get_json()
        print(feature_data)
        for key in feature_data.keys():
            feature_data[key] = [feature_data[key]]

        predictions = model.predict(pd.DataFrame(feature_data))
        print(predictions)

        requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "success"})

        with open('./model/label_int_tag.json', 'rb') as f:
            label_int_tag_json = json.load(f)
        decoded_labels = [label_int_tag_json["int_to_label"][str(i)] for i in predictions]

        return {"code": 0, "data": decoded_labels}


# except Exception as e:
#     print(e)
#     requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
#                   json={"task_id": config["taskId"], "operation": "fail"})
#
#     return {"code": -1, "data": str(e)}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
