import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from trueTrace import trueTraceBP

app = Flask(__name__)
CORS(app)

app.register_blueprint(trueTraceBP, url_prefix="/truetrace")

if __name__ == "__main__":
    app.run(port=2497)