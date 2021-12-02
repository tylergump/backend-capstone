from flask import Flask, g
from flask_cors import CORS

import models
from resources.goals import goals

DEBUG = True
PORT = 8000

#initialize Flask class and start website
app = Flask(__name__)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(goals, origins=['http://localhost:3000'], supports_credentials=True) 


app.register_blueprint(goals, url_prefix='/api/v1/goals')

@app.route('/')
def index():
    return 'hi'



#run app when program starts
if __name__== '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)