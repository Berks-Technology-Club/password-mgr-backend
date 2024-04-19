import os
import json
import datetime
from dbhelper import dbhelper
from flask import Flask, request
from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity

app = Flask(__name__)

load_dotenv()
mongo_user = os.getenv("mongo_user")
mongo_pass = os.getenv("mongo_passwd")

uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@passdb.qcojh7t.mongodb.net/?retryWrites=true&w=majority&appName=PassDB"

helper = dbhelper()
helper.connect(uri)


jwt_secret = os.getenv("jwt_secret")
app.config["JWT_SECRET_KEY"] = jwt_secret
jwt = JWTManager(app)

invalid_jwt = set()

def validate_jwt_token(jwt_token):
    if jwt_token in invalid_jwt:
        return False
    return True

def get_jwt_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        # Check if the header follows the 'Bearer' scheme
        if 'Bearer ' in auth_header:
            token = auth_header.split()[1]  # Extract token after 'Bearer '
            return token
        else:
            # Handle case where format is not 'Bearer token'
            return None
    else:
        # No authorization header present
        return None

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
    timeout = datetime.timedelta(hours=2)
    access_token = create_access_token(identity=username, additional_claims=additional_claims, expires_delta=timeout)
    
    return jsonify(access_token=access_token)

@app.route("/protected")
@jwt_required()
def protected():
    return get_jwt()


@app.route("/get_passwords")
@jwt_required()
def get_passwords():
    if validate_jwt_token(get_jwt_token()):
        passwords = helper.get_passwords()
        return json.dumps(passwords, default=str)
    
    resp = json.dumps({"msg": "invalid jwt token"})
    return resp, 401



@app.route("/logout")
@jwt_required()
def logout():
    resp = jsonify({'logout': True})
    invalid_jwt.add(get_jwt_token())
    return resp, 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)