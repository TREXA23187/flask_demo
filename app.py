from flask import Flask, render_template, request
from model.enter import run
import json
import requests
import base64
import pickle
import pandas as pd
import os

from utils.eda import data_summary, descriptive_statistics, correlation_matrix
from utils.evaluate import confusion_matrix

app = Flask(__name__)

localhost = "host.docker.internal:8080"
# localhost = "localhost:8080"
# localhost = "47.243.60.114:3000"

dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/data.csv"))

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
        requests.post(f'http://{localhost}/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "success",
                            "model_file": model_file_base64, "label_int_tag": json.dumps(label_int_tag)})
    except Exception as e:
        print("error: ", e)
        model_evaluation = {}
        requests.post(f'http://{localhost}/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    if config["type"] == "training":
        data_head, data_info = data_summary(dataset)
        data_describe = descriptive_statistics(dataset)
        corr_matrix_image_path = "static/corr_matrix.png"
        correlation_matrix(dataset.drop([config["targetLabel"]], axis=1), corr_matrix_image_path)

        eda = {
            "data_head": data_head.to_html(),
            "data_info": data_info.to_html(),
            "data_describe": data_describe.to_html(),
            "corr_matrix_image": corr_matrix_image_path
        }

        confusion_matrix_image_path = "static/confusion_matrix.png"
        confusion_matrix(cm=model_evaluation["confusion_matrix"], labels=dataset[config["targetLabel"]].unique(),
                         image_save_path=confusion_matrix_image_path)

        model_evaluation_html = {
            "model_evaluation_report": pd.DataFrame(model_evaluation["classification_report"]).T.to_html(),
            "confusion_matrix_image": confusion_matrix_image_path
        }
        if model_evaluation["optimal_hyper_parameters"]:
            optimal_hyper_parameters = pd.DataFrame(model_evaluation["optimal_hyper_parameters"],
                                                    index=model_evaluation["optimal_hyper_parameters"].keys()).T
            optimal_hyper_parameters = optimal_hyper_parameters.iloc[:, 0:1]
            optimal_hyper_parameters.columns = ["value"]

            model_evaluation_html["optimal_hyper_parameters"] = optimal_hyper_parameters.to_html()

        return render_template("index.html", config=config, model_evaluation=model_evaluation_html, eda=eda)


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

            requests.post(f'http://{localhost}/api/v1/console/task/operate',
                          json={"task_id": config["taskId"], "operation": "success"})

            with open('./model/label_int_tag.json', 'r') as label_int_tag_file:
                label_int_tag_json = json.load(label_int_tag_file)
            decoded_labels = [label_int_tag_json["int_to_label"][str(i)] for i in predictions]

            return {"code": 0, "data": decoded_labels}
    except Exception as e:
        print(e)
        requests.post(f'http://{localhost}/api/v1/console/task/operate',
                      json={"task_id": config["taskId"], "operation": "fail"})

        return {"code": -1, "msg": str(e)}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
