from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)  # Make sure this line exists and is correctly defined

# Load the OpenWeatherMap API key from environment variables
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    try:
        # Fetch weather data from OpenWeatherMap API
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        )
        data = response.json()

        if response.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch data')}), response.status_code

        weather_info = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
        }

        return jsonify(weather_info), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
