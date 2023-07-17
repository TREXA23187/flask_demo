from flask import Flask, render_template
from model.enter import run
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('config.json', 'r', encoding='utf-8') as fp:
        config = json.load(fp)

    model_evaluation = run()
    return render_template("index.html", config=config, model_evaluation=model_evaluation)


@app.route('/model')
def model():
    return "model test"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
