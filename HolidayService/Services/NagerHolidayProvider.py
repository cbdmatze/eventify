from HolidayService.Interface.IHolidayProvider import IHolidayProvider
import requests
from datetime import datetime, timedelta

class NagerHolidayProvider(IHolidayProvider):
    """
    A holiday provider that fetches holiday data from the Nager Holiday API.
    """

    BASE_URL = "https://date.nager.at/Api/V3"

    def get_holidays(self, year: int, country_code: str):
        """
        Fetches the holidays for a specific year and country code.

        Args:
            year (int): The year to fetch holidays for.
            country_code (str): The country code to fetch holidays for.

        Returns:
            list: A list of holidays for the specified year and country code.
        """
        url = f"{self.BASE_URL}/PublicHolidays/{year}/{country_code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch holidays: {response.status_code}, {response.text}")

    def get_next_week_holidays(self, year: int, **kwargs):
        """
        Fetches the holidays that fall within the next week from today.

        Args:
            year (int): The year to fetch holidays for.
            **kwargs: Additional keyword arguments, including country_code.

        Returns:
            list: A list of holidays falling in the next week.
        """
        country_code = kwargs.get("country_code", None)

        url = f"{self.BASE_URL}/PublicHolidays/{year}/{country_code}"
        print(url)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch holidays: {response.status_code}")

        holidays = response.json()
        today = datetime.today()
        next_week = today + timedelta(days=7)

        next_week_holidays = [
            holiday for holiday in holidays
            if today < datetime.strptime(holiday["date"], "%Y-%m-%d") <= next_week
        ]
        return next_week_holidays

    def get_next365_holidays(self, country_code: str, **kwargs):
        """
        Fetches the next 365 days' worth of holidays for a given country.

        Args:
            country_code (str): The country code to fetch holidays for.
            **kwargs: Additional keyword arguments, if needed.

        Returns:
            list: A list of the next 365 holidays.
        """
        url = f"{self.BASE_URL}/NextPublicHolidays/{country_code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch holidays: {response.status_code}, {response.text}")
