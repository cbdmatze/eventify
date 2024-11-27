import requests
import json

class HolidayService:
    """
    Service class for interacting with the Holiday API to fetch upcoming holidays.
    """

    def __init__(self, api_key: str):
        """
        Initializes the HolidayService with the given API key.

        Args:
            api_key (str): The API key for the Holiday API.
        """
        self.api_key = api_key
        self.api_url = "https://holidayapi.com/v1/holidays"

    def get_next_holiday(self, country: str, year: int, month: int):
        """
        Fetches the next upcoming holiday from the Holiday API.

        Args:
            country (str): The country code (e.g., 'US') to fetch holidays for.
            year (int): The year for which to fetch holidays.
            month (int): The starting month to look for holidays.

        Returns:
            dict: The next holiday details, or None on failure.
        """
        params = {
            'key': self.api_key,
            'country': country,
            'year': year,
            'month': month,
            'upcoming': 'true'
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            holidays = response.json().get('holidays', [])
            next_holiday = holidays[0] if holidays else None
            self.save_holiday_data_to_json(next_holiday, 'data/user_data.json')
            return next_holiday
        else:
            print(f"Error fetching holidays: {response.status_code}")
            return None

    def save_holiday_data_to_json(self, holiday: dict, filename: str):
        """
        Saves the holiday data to a JSON file.

        Args:
            holiday (dict): The holiday details to save.
            filename (str): The file to save the holiday data to.
        """
        try:
            with open(filename, 'r+') as file:
                data = json.load(file)
                data['holiday'] = holiday
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                json.dump({'holiday': holiday}, file, indent=4)
