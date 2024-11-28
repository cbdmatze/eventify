import requests
import json

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    def get_weather_data(self, location, user_phone):
        url = f"{self.base_url}{location}"

        params = {
            'key': self.api_key,
            'unitGroup': 'metric',
            'include': 'current',
            'contentType': 'json'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            self.save_user_data(user_phone, {'weather': weather_data})
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Visual Crossing API: {e}")
            return None

    def save_user_data(self, user_phone, data):
        try:
            # Load existing data
            with open('data/user_data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        # Update user data with new data
        if user_phone not in user_data:
            user_data[user_phone] = {}
        
        user_data[user_phone].update(data)

        # Save back to user_data.json
        with open('data/user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
