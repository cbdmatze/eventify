import requests
import json
from datetime import datetime


class HolidayService:
    def __init__(self, api_key):
        self.api_url = "https://holidayapi.com/v1/holidays"
        self.api_key = api_key  

    def get_holidays(self, country, year):
        """
        Fetch holidays for the given country and year.
        """
        params = {
            'apikey': self.api_key, 
            'country': country,
            'year': year,
            'public': True,  
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            holiday_data = response.json()  
            self.save_holiday_data_to_file(holiday_data)  # Save to JSON file
            return holiday_data['holidays']
        else:
            print(f"Error fetching holidays: {response.status_code}")
            return None

    def save_holiday_data_to_file(self, holiday_data):
        """
        Save the raw holiday data to a file called 'holiday_data.json'.
        """
        try:
            with open('holiday_data.json', 'w') as file:
                json.dump(holiday_data, file, indent=4)  
            print("Holiday data saved to 'holiday_data.json'.")
        except IOError as e:
            print(f"Error saving holiday data to file: {e}")

    def get_upcoming_holiday(self, holidays):
        """
        Get the next upcoming holiday based on today's date.
        """
        today = datetime.now().date()
        upcoming_holidays = []

        for holiday in holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
            if holiday_date >= today:
                upcoming_holidays.append((holiday['name'], holiday_date))

        if upcoming_holidays:
            upcoming_holidays.sort(key=lambda x: x[1])  # Sort by date
            return upcoming_holidays[0]  # Return the closest upcoming holiday
        else:
            return None


if __name__ == "__main__":
    api_key = 'fd8817e4-9ca4-4012-9dfc-c4dbe6d1f81c'  
    country = "DE"  # Example: Germany (ISO 3166-1 alpha-2 country code)
    year = datetime.now().year

    # Create an instance of the HolidayService
    holiday_service = HolidayService(api_key)

    # Fetch holidays and store them in 'holiday_data.json'
    holidays = holiday_service.get_holidays(country, year)

    if holidays:
        # Print the next upcoming holiday
        upcoming_holiday = holiday_service.get_upcoming_holiday(holidays)  

        if upcoming_holiday:
            holiday_name, holiday_date = upcoming_holiday
            print(f"The next upcoming holiday is {holiday_name} on {holiday_date}.")
        else:
            print("No upcoming holidays found.")
    else:
        print("Failed to retrieve holidays.")
