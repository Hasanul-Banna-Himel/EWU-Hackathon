from flask import *
import requests
# Prediction client
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
# Key class for azure
from msrest.authentication import ApiKeyCredentials
# dotenv to load key
from dotenv import load_dotenv
# Import os to read environment variables
import os

# Load the key and endpoint values
load_dotenv()



app = Flask(__name__)

open_weather_api = os.getenv("OpenWeather_API_KEY")
geo_api = os.getenv("GeoAPI_API_KEY")
key = os.getenv('Prediction_KEY')
endpoint = os.getenv('Prediction_ENDPOINT')
project_id = os.getenv('Project_ID')
published_name = os.getenv('Iteration_name')

def get_ip():
    response = requests.get('https://api.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://api.getgeoapi.com/v2/ip/{ip_address}?api_key={geo_api}&format=json&language=en').json()

    return response

def get_weather():
    pass

def get_prediction():
    # Setup credentials for client
    credentials = ApiKeyCredentials(in_headers={'Prediction-key':key})

    # Create client, which will be used to make predictions
    client = CustomVisionPredictionClient(endpoint, credentials)

    # Open the test file
    with open('static/images/test.JPG', 'rb') as image:
        # Perform the prediction
        results = client.classify_image(project_id, published_name, image.read())


        # Because there could be multiple predictions, we loop through each one
        
        for i in range(len(results.predictions)):


@app.route("/")
def home():
    data = get_location()
    return data


if __name__ == "__main__": 
    app.run(debug=True)