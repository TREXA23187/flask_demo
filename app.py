from flask import Flask, render_template
from model.enter import run
import json
import requests

app = Flask(__name__)

with open('config.json', 'r', encoding='utf-8') as fp:
    config = json.load(fp)

try:
    model_evaluation = run(config)
    response = requests.post('http://localhost:8080/api/v1/console/task/operate',
                             json={"task_id": config["taskId"], "operation": "success"})
except Exception as e:
    print(e)
    response = requests.post('http://localhost:8080/api/v1/console/task/operate',
                             json={"task_id": config["taskId"], "operation": "fail"})


@app.route('/')
def index():
    return render_template("index.html", config=config, model_evaluation=model_evaluation)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
