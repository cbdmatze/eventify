
from abc import ABC, abstractmethod

class IHolidayProvider(ABC):
    """
    Abstract base class for holiday providers, defining the required methods for fetching holidays.
    """

    @abstractmethod
    def get_holidays(self, year: int, country_code: str):
        """
        Fetch holidays for a specific year and country.

        Args:
            year (int): The year to fetch holidays for.
            country_code (str): The country code to fetch holidays for.

        Returns:
            list: A list of holidays for the given year and country.
        """
        pass

    @abstractmethod
    def get_next365_holidays(self, country_code: str):
        """
        Fetch holidays for the next 365 days for a given country.

        Args:
            country_code (str): The country code to fetch holidays for.

        Returns:
            list: A list of holidays for the next 365 days.
        """
        pass
