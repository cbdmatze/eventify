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
    def __init__(self, provider: IHolidayProvider):
        self.provider = provider

    def get_state_name(self, state_number):
        return DE_STATES.get(state_number, None)

    def get_holidays(self, year: int, country_code: str):
        return self.provider.get_holidays(year, country_code)

    def get_next365_holidays(self, country_code: str):
        return self.provider.get_next365_holidays(country_code)

def main():
    holiday_provider = NagerHolidayProvider()
    HolidayService = HolidayController(holiday_provider)
    print(HolidayService.get_holidays(year=2024, country_code=DE_COUNTRY_CODE))
    print(HolidayService.get_next365_holidays(country_code=DE_COUNTRY_CODE))

if __name__ == "__main__":
    main()


