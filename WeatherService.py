import requests
import json

class WeatherService:
    """
    Service class for interacting with the Visual Crossing Weather API to fetch weather forecasts.
    """

    def __init__(self, api_key: str):
        """
        Initializes the WeatherService with the given API key.

        Args:
            api_key (str): The API key for the Visual Crossing Weather API.
        """
        self.api_key = api_key
        self.api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    def get_weather_forecast(self, city: str, start_date: str):
        """
        Fetches a 7-day weather forecast from Visual Crossing for the given city and start date.

        Args:
            city (str): The city to fetch the forecast for.
            start_date (str): The start date for the forecast in 'YYYY-MM-DD' format.

        Returns:
            list: A list of weather forecast details, or None on failure.
        """
        params = {
            'unitGroup': 'metric',
            'key': self.api_key,
            'include': 'days'
        }

        api_url = f"{self.api_url}{city}/{start_date}/next7days"

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            forecast_data = response.json()
            forecasts = self.extract_forecast_info(forecast_data)
            self.save_weather_data_to_json(forecasts, 'data/user_data.json')
            return forecasts
        else:
            print(f"Error fetching weather data: {response.status_code}")
            return None

    def extract_forecast_info(self, forecast_data: dict):
        """
        Extracts relevant weather information from the API response.

        Args:
            forecast_data (dict): The raw forecast data from the Weather API.

        Returns:
            list: A list of daily weather details with relevant information.
        """
        forecasts = []
        for day in forecast_data['days']:
            forecasts.append({
                'date': day.get('datetime', 'Date not available'),
                'temp': day.get('temp', 'Temp not available'),
                'description': day.get('description', 'Description not available')
            })
        return forecasts

    def save_weather_data_to_json(self, forecasts: list, filename: str):
        """
        Saves the weather forecast data to a JSON file.

        Args:
            forecasts (list): The weather forecast details to save.
            filename (str): The file to save the weather data to.
        """
        try:
            with open(filename, 'r+') as file:
                data = json.load(file)
                data['weather'] = forecasts
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                json.dump({'weather': forecasts}, file, indent=4)
