import json
from datetime import datetime
from HolidayService.Interface.IHolidayProvider import IHolidayProvider
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider

# Define the German states (DE_STATES) dictionary
DE_STATES = {
    1: 'Baden-Württemberg',
    2: 'Bayern',
    3: 'Berlin',
    4: 'Brandenburg',
    5: 'Bremen',
    6: 'Hamburg',
    7: 'Hessen',
    8: 'Mecklenburg-Vorpommern',
    9: 'Niedersachsen',
    10: 'Nordrhein-Westfalen',
    11: 'Rheinland-Pfalz',
    12: 'Saarland',
    13: 'Sachsen',
    14: 'Sachsen-Anhalt',
    15: 'Schleswig-Holstein',
    16: 'Thüringen'
}

class HolidayController:
    def __init__(self, provider: IHolidayProvider):
        self.provider = provider

    def get_state_name(self, state_number):
        """Returns the state name based on the state number."""
        return DE_STATES.get(state_number, None)

    def get_holidays(self, year: int, country_code: str, user_phone: str):
        """Fetches holidays for the given year and country code, then saves to user data."""
        holidays = self.provider.get_holidays(year, country_code)
        self.save_user_data(user_phone, {'holidays': holidays})
        return holidays

    def get_next365_holidays(self, country_code: str, user_phone: str):
        """Fetches holidays for the next 365 days for the given country code, then saves to user data."""
        holidays = self.provider.get_next365_holidays(country_code)
        self.save_user_data(user_phone, {'holidays': holidays})
        return holidays

    def save_user_data(self, user_phone, data):
        """Saves the fetched holiday data to user_data.json under the specific user's phone number."""
        try:
            # Load existing user data
            with open('data/user_data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        # Update user data with the new data
        if user_phone not in user_data:
            user_data[user_phone] = {}

        user_data[user_phone].update(data)

        # Save the updated data back to user_data.json
        with open('data/user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
