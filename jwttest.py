from flask import Flask, request
from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
load_dotenv()
app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "secret"  # Change this!
jwt = JWTManager(app)

@app.route("/")
def home():
    return "home"


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(identity=username, additional_claims=additional_claims, expires_delta=False)
    
    return jsonify(access_token=access_token)

@app.route("/test")
def test():
    return "This is a test path"

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    
    return  "This is a protected path"


if __name__ == "__main__":
    app.run(debug=True)