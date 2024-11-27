
import requests
import json

# WeatherService Class to fetch weather data
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    def get_weather_data(self, location):
        url = f"{self.base_url}{location}"

        # Set up query parameters
        params = {
            'key': self.api_key,
            'unitGroup': 'metric',  # Use 'us' for Fahrenheit, 'metric' for Celsius
            'include': 'current',   # Get current weather data
            'contentType': 'json'
        }
        
        try:
            # Send the request to the API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            weather_data = response.json()  # Parse the JSON response
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Visual Crossing API: {e}")
            return None

# WeatherDataStorage Class to handle saving data to a file
class WeatherDataStorage:
    @staticmethod
    def save_weather_data_to_json(weather_data, filename):
        try:
            # Write the weather data to a file in JSON format
            with open(filename, 'w') as json_file:
                json.dump(weather_data, json_file, indent=4)
            print(f"Weather data saved to {filename}")
        except IOError as e:
            print(f"Error saving data to file: {e}")

    @staticmethod
    def load_weather_data_from_json(filename):
        try:
            # Read the weather data from the JSON file
            with open(filename, 'r') as json_file:
                return json.load(json_file)
        except IOError as e:
            print(f"Error loading data from file: {e}")
            return None

# Main Application
class WeatherApp:
    def __init__(self, api_key):
        self.weather_service = WeatherService(api_key)
        self.weather_storage = WeatherDataStorage()

    def fetch_and_save_weather(self, location, filename):
        weather_data = self.weather_service.get_weather_data(location)
        if weather_data:
            self.weather_storage.save_weather_data_to_json(weather_data, filename)

    def display_current_weather(self, filename):
        weather_data = self.weather_storage.load_weather_data_from_json(filename)
        if weather_data and 'currentConditions' in weather_data:
            current_weather = weather_data['currentConditions']
            print(f"Current Weather:")
            print(f"Temperature: {current_weather.get('temp', 'N/A')}°C")
            print(f"Conditions: {current_weather.get('conditions', 'N/A')}")
            print(f"Humidity: {current_weather.get('humidity', 'N/A')}%")
            print(f"Wind Speed: {current_weather.get('wspd', 'N/A')} km/h")
        else:
            print("Current weather data not found in the file.")

if __name__ == "__main__":
    # Example location and your API key
    location = "Berlin"  # You can change this to any city or postal code
    api_key = "6R6EZ6N2WTV4PX5JXP84SJQX4"
    
    # Create the WeatherApp instance and fetch/save the weather data
    weather_app = WeatherApp(api_key)
    weather_app.fetch_and_save_weather(location, 'data/weather_data.json')
   
    # Now display the current weather from the saved JSON
    weather_app.display_current_weather('data/weather_data.json')
