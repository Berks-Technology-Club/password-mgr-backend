import os
import json
from dbhelper import dbhelper
from flask import Flask, request
from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt

app = Flask(__name__)

load_dotenv()
mongo_user = os.getenv("mongo_user")
mongo_pass = os.getenv("mongo_passwd")

uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@passdb.qcojh7t.mongodb.net/?retryWrites=true&w=majority&appName=PassDB"

helper = dbhelper()
helper.connect(uri)


app.config["JWT_SECRET_KEY"] = "secret"  # Change this!
jwt = JWTManager(app)

@app.route("/")
def home():
    result = 6+7
    return str(result)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(identity=username, additional_claims=additional_claims, expires_delta=False)
    
    return jsonify(access_token=access_token)

@app.route("/protected")
@jwt_required()
def protected():
    return "this is a protected path."


@app.route("/get_passwords")
def get_passwords():
    passwords = helper.get_passwords()
    return json.dumps(passwords, default=str)
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)