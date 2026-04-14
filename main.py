from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from trueTrace import trueTraceBP
from ecoFuture import ecoFutureBP
from terralytics import terralyticsBP

app = Flask(__name__)
# ALLOWED_ORIGINS = [
#     "http://127.0.0.1:5500",
#     "http://localhost:5500",
#     "https://truetracenjx.pages.dev",
#     "https://ecofuture.pages.dev",
#     "https://terralytics.pages.dev"
# ]
CORS(app)

app.register_blueprint(trueTraceBP, url_prefix="/truetrace")
app.register_blueprint(ecoFutureBP, url_prefix="/ecofuture")
app.register_blueprint(terralyticsBP, url_prefix="/terralytics")

if __name__ == "__main__":
    app.run(port=2497)