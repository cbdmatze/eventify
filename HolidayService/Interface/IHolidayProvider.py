from abc import ABC, abstractmethod

class IHolidayProvider(ABC):
    @abstractmethod
    def get_holidays(self, year: int, **kwargs):
        pass
    @abstractmethod
    def get_next_week_holidays(self, year: int, **kwargs):
        pass



