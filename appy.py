from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    result = 6+7
    return str(result)

@app.route("/login")
def login():
    return "<h1> login page"


if __name__ == "__main__":
    app.run(host="127.0.0.1")