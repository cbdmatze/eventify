from abc import ABC, abstractmethod

class IHolidayProvider(ABC):
    """
    Abstract base class for holiday providers, defining the required methods for fetching holidays.
    """

    @abstractmethod
    def get_holidays(self, year: int, **kwargs):
        """
        Fetch holidays for a specific year and country.

        Args:
            year (int): The year to fetch holidays for.
            kwargs: Additional parameters, such as country code.

        Returns:
            list: A list of holidays for the given year and country.
        """
        pass

    @abstractmethod
    def get_next_week_holidays(self, year: int, **kwargs):
        """
        Fetch holidays in the next week for a given year.

        Args:
            year (int): The year to fetch holidays for.
            kwargs: Additional parameters, such as country code.

        Returns:
            list: A list of holidays in the next week.
        """
        pass
