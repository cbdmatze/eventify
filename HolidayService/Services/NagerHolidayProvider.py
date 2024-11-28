from HolidayService.Interface.IHolidayProvider import IHolidayProvider
import requests
from datetime import datetime, timedelta

class NagerHolidayProvider(IHolidayProvider):
    BASE_URL = "https://date.nager.at/Api/V3"

    def get_holidays(self, year: int, country_code: str):
        url = f"{self.BASE_URL}/PublicHolidays/{year}/{country_code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch holidays: {response.status_code}, {response.text}")

    def get_next365_holidays(self, country_code: str):
        url = f"{self.BASE_URL}/NextPublicHolidays/{country_code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch holidays: {response.status_code}, {response.text}")
