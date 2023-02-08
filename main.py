from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "1234"
DATABASE = "bonus"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)


class Uesr(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


# 测试是否连接成功
with app.app_context():
    # with db.engine.connect() as con:
    #     query = "SELECT 1;"
    #     result = con.execute(text(query))
    #     print(result.fetchone())
    # user = Uesr(username="test", password="test")
    db.create_all()


@app.route("/test/add")
def add_test():
    user = Uesr(username="test1", password="test1")
    db.session.add(user)
    db.session.commit()

    return "add test"


@app.route("/")
def index():
    return "hello world123"


@app.route("/say_hello/<name>")
def say_hello(name):
    return "hello world,I am your friend %s" % name


if __name__ == "__main__":
    app.run(debug=True)
