from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "beb6ae1a9367bec7eb4a8e8d9a300a91"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get("city")
        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].capitalize()
                }
            else:
                weather_data = {"error": data.get("message", "Failed to fetch weather data")}
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
