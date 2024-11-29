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

    def get_weather(self, city: str = None, postal_code: str = None):
        """
        Fetches the weather forecast based on the city or postal code from Visual Crossing.

        Args:
            city (str, optional): The city for which to fetch weather. Defaults to None.
            postal_code (str, optional): The postal code for which to fetch weather. Defaults to None.

        Returns:
            dict: The weather forecast details, or None on failure.
        """
        if not city and not postal_code:
            raise ValueError("Either city or postal code must be provided.")

        params = {
            'unitGroup': 'metric',
            'key': self.api_key,
            'include': 'days'
        }

        if city:
            api_url = f"{self.api_url}{city}/next7days"
        elif postal_code:
            api_url = f"{self.api_url}{postal_code}/next7days"

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching weather data: {http_err}")
            print(f"Response Content: {response.text}")  # Log the response content for debugging
        except Exception as err:
            print(f"Other error occurred while fetching weather data: {err}")
        else:
            if response.status_code == 200:
                forecast_data = response.json()
                forecasts = self.extract_forecast_info(forecast_data)
                self.save_weather_data_to_json(forecasts, 'data/user_data.json')
                return forecasts
            else:
                print(f"Error fetching weather data: {response.status_code}")
                print(f"Response Content: {response.text}")  # Log the response content for debugging
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
        if 'days' in forecast_data:
            for day in forecast_data['days']:
                forecasts.append({
                    'date': day.get('datetime', 'Date not available'),
                    'temp': day.get('temp', 'Temp not available'),
                    'description': day.get('description', 'Description not available')
                })
        else:
            print("No weather data available.")
        return forecasts

    def save_weather_data_to_json(self, forecasts: list, filename: str):
        """
        Saves the weather forecast data to a JSON file.

        Args:
            forecasts (list): The weather forecast details to save.
            filename (str): The file to save the weather data to.
        """
        try:
            # Open the file and update the weather data
            with open(filename, 'r+') as file:
                data = json.load(file)
                data['weather'] = forecasts
                file.seek(0)  # Rewind to the beginning of the file
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            # If file doesn't exist, create a new file with weather data
            with open(filename, 'w') as file:
                json.dump({'weather': forecasts}, file, indent=4)

    def get_saved_weather(self, filename: str):
        """
        Retrieves the saved weather data from the JSON file.

        Args:
            filename (str): The file to retrieve the weather data from.

        Returns:
            dict: The saved weather data or an empty dict if not found.
        """
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return data.get('weather', [])
        except FileNotFoundError:
            print(f"No weather data found in {filename}.")
            return []
