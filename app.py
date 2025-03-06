from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "77a5c959c3dd0697c3a96be80e81a5b8" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
IP_GEO_URL = "http://ip-api.com/json/"  


def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if response.status_code == 200:
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
        }
    else:
        return {"error": data.get("message", "Failed to fetch weather data")}


def get_forecast(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(FORECAST_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        forecast_list = []
        for item in data["list"][:5]:  # Fetch next 5 forecasts (3-hour intervals)
            forecast_list.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"].capitalize()
            })
        return forecast_list
    else:
        return [{"error": data.get("message", "Failed to fetch forecast data")}]

def get_location_weather():
    ip_data = requests.get(IP_GEO_URL).json()
    city = ip_data.get("city", "Unknown")
    if city and city != "Unknown":
        return get_weather(city)
    return {"error": "Unable to determine location"}

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    forecast_data = None
    location_weather = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_data = get_weather(city)
            forecast_data = get_forecast(city)

    location_weather = get_location_weather()  

    return render_template("index.html", weather_data=weather_data, forecast_data=forecast_data, location_weather=location_weather)

if __name__ == "__main__":
    app.run(debug=True)
