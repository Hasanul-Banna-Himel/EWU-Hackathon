from flask import *
import requests
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid


app = Flask(__name__)

open_weather_api = os.getenv("OpenWeather_API_KEY")
prediction_key = os.getenv("Prediction_KEY")
prediction_endpoint = os.getenv("Prediction_ENDPOINT")
training_key = os.getenv("Training_KEY")
training_endpoint = os.getenv("Training_ENDPOINT")

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://api.getgeoapi.com/v2/ip/{ip_address}?api_key={geo_api}&format=json&language=en').json()
    return response

@app.route("/")
def home():
    data = get_location()
    return render_template("index.html")

if __name__ == "__main__": 
    app.run(debug=True)