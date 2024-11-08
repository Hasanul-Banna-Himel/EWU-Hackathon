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
import google.generativeai as genai
from werkzeug.utils import secure_filename


# Load the key and endpoint values
load_dotenv()
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'jpg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


open_weather_api = os.getenv("OpenWeather_API_KEY")
geo_api = os.getenv("GeoAPI_API_KEY")
gemini_api = os.getenv("Gemini_API_KEY")
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
    with open('uploads/test.JPG', 'rb') as image:
        # Perform the prediction
        results = client.classify_image(project_id, published_name, image.read())
        info = {}
        probabilities = []




        # Because there could be multiple predictions, we loop through each one
        for prediction in results.predictions:
            # Display the name of the breed, and the probability percentage


            info[prediction.probability] = prediction.tag_name
            probabilities.append(prediction.probability)


    disease = info[max(probabilities)]
    return disease


def get_suggestion():
    disease = get_prediction()
    genai.configure(api_key=gemini_api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Pretend to be an agriculturalist who specializes in corn, potatoes and tomatoes production in Bangladesh. You talk to the farmers of Bangladesh. Give simple and short steps in which farmers can save their crops from {disease}.")
    suggestion = response.text
    return suggestion


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))


    disease = get_prediction()
    suggestion = get_suggestion()
    return render_template("index.html", disease=disease, suggestion=suggestion)




if __name__ == "__main__":
    app.run(debug=True)