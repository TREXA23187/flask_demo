from flask import Flask, render_template
from model.enter import run
import json
import requests
import sys

app = Flask(__name__)

localhost = "host.docker.internal"
# localhost = "47.243.60.114"

with open('config.json', 'r', encoding='utf-8') as fp:
    config = json.load(fp)

try:
    model_evaluation = run(config)

    with open('./model/model.pickle', 'rb') as f:
        model_file = f.read()
    response = requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                             json={"task_id": config["taskId"], "operation": "success", "model_file": model_file})
except Exception as e:
    print(e)
    response = requests.post(f'http://{localhost}:8080/api/v1/console/task/operate',
                             json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    return render_template("index.html", config=config, model_evaluation=model_evaluation)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
