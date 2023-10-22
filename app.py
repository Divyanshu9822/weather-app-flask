from flask import Flask, render_template, request
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
BASE_URL = os.environ.get("BASE_URL")

def get_weather_by_coords(lat, lon):
    base_url = BASE_URL
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def get_weather_by_city(city):
    base_url = BASE_URL
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code != 200:
        return None
    return data

def get_formatted_date():
    current_date = datetime.now().strftime("%A %d %B %Y")
    return current_date

@app.route("/", methods=["GET", "POST"])
def index():
    lat, lon = None, None
    city_name = None
    weather_data = None
    error = None

    if request.method == "POST":
        city_name = request.form.get("city_name")
        if city_name:
            weather_data = get_weather_by_city(city_name)
            if weather_data is None:
                error = f"City not found: {city_name}"
        else:
            error = "Please enter a city name."

    if not weather_data and error is None:
        city_name = "Paris"
        weather_data = get_weather_by_city(city_name)

    current_date = get_formatted_date()

    return render_template(
        "index.html",
        weather_data=weather_data,
        city_name=city_name,
        current_date=current_date,
        error=error  # Pass the error message to the template
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
