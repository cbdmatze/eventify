from HolidayService.Interface.IHolidayProvider import IHolidayProvider
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from datetime import datetime, timedelta

DE_COUNTRY_CODE = "DE"
DE_STATES = {
    1: ("DE-BW", "Baden-Württemberg"),
    2: ("DE-BY", "Bayern"),
    3: ("DE-BE", "Berlin"),
    4: ("DE-BB", "Brandenburg"),
    5: ("DE-HB", "Bremen"),
    6: ("DE-HH", "Hamburg"),
    7: ("DE-HE", "Hessen"),
    8: ("DE-MV", "Mecklenburg-Vorpommern"),
    9: ("DE-NI", "Niedersachsen"),
    10: ("DE-NW", "Nordrhein-Westfalen"),
    11: ("DE-RP", "Rheinland-Pfalz"),
    12: ("DE-SL", "Saarland"),
    13: ("DE-SN", "Sachsen"),
    14: ("DE-ST", "Sachsen-Anhalt"),
    15: ("DE-SH", "Schleswig-Holstein"),
    16: ("DE-TH", "Thüringen")
}

class HolidayController:
    """
    Controller for handling holiday-related operations using a holiday provider.
    """

    def __init__(self, provider: IHolidayProvider):
        """
        Initializes the HolidayController with a holiday provider.

        Args:
            provider (IHolidayProvider): An instance of a holiday provider.
        """
        self.provider = provider

    def get_state_name(self, state_number):
        """
        Returns the name of the state corresponding to the given state number.

        Args:
            state_number (int): The state number.

        Returns:
            tuple: A tuple containing the state code and name, or None if not found.
        """
        return DE_STATES.get(state_number, None)

    def get_holidays(self, year: int, country_code: str):
        """
        Fetches holidays for a specific year and country code.

        Args:
            year (int): The year to fetch holidays for.
            country_code (str): The country code for the holidays (e.g., "DE" for Germany).

        Returns:
            list: A list of holidays for the given year and country code.
        """
        if not isinstance(year, int) or year <= 0:
            raise ValueError("Invalid year.")
        if not country_code:
            raise ValueError("Country code cannot be empty.")
        return self.provider.get_holidays(year, country_code)

    def get_next365_holidays(self, country_code: str):
        """
        Fetches the next 365 holidays for the given country code.

        Args:
            country_code (str): The country code to fetch holidays for.

        Returns:
            list: A list of the next 365 holidays for the given country code.
        """
        if not country_code:
            raise ValueError("Country code cannot be empty.")
        return self.provider.get_next365_holidays(country_code)
