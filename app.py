from flask import Flask, render_template
from model.enter import run
import json

app = Flask(__name__)


@app.route('/')
def index():
    run()
    return render_template("index.html")


@app.route('/model')
def model():
    model_evaluation = run()
    return json.dumps(model_evaluation)


if __name__ == "__main__":
    app.run(debug=True)
