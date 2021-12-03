from flask import Flask, jsonify
from flask_cors import CORS
from resources.goals import goals
from resources.users import users
from flask_login import LoginManager
import models

import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = ("FLASK_APP_SECRET")  # new
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    print("unauthorized")
    return (
        jsonify(
            data={"error": "User not logged in"},
            message="You must be logged in to access that resource",
            status=401,
        ),
        401,
    )


CORS(goals, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(goals, url_prefix="/api/v1/goals")
app.register_blueprint(users, url_prefix="/api/v1/users")


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/test_json")
def get_json():
    return jsonify(["hello", "hi", "hey"])


@app.route("/cat_json")
def get_cat_json():
    return jsonify(name="King Charles III", age=6)


@app.route("/nested_json")
def get_nested_json():
    cat_dict = {
        "name": "King Charles III",
        "age": 6,
        "cute": True,
        "sweet": True,
    }
    return jsonify(name="Deja Y", age=25, cat=cat_dict)


@app.route("/two_cats")
def get_two_cats():
    sir = {
        "name": "King Charles III",
        "age": 6,
        "cute": True,
        "sweet": True,
    }
    bens_cat = {
        "name": "Lady Jeffery",
        "age": 7,
        "cute": True,
        "sweet": False,
    }
    return jsonify(name="Deja Y", age=25, cats=[sir, bens_cat])


@app.route("/say_hello/<username>")
def say_hello(username):
    return f"Hello {username}"


# Run the app when the program starts!
if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
