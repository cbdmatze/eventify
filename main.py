import json
from datetime import datetime, timedelta
from SMSService.Controller.SMSController import SMSController
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from HolidayService.Controller.HolidayController import HolidayController
from EventService import EventService
from WeatherService import WeatherService

# Constants
API_KEY_TICKETMASTER = "8yHnQv1827D9Gtj6HhnmDIqLBU2zB4CA"
API_KEY_WEATHER = "HLU729E56SMY3M2FCQJLCXEYM"

# Main application logic
class MainApp:
    def __init__(self):

        self.SMSService = SMSController()
        self.sms_provider = SMSController()
        self.holiday_provider = NagerHolidayProvider()
        self.holiday_service = HolidayController(self.holiday_provider)

        self.event_service = EventService(API_KEY_TICKETMASTER)
        self.weather_app = WeatherService(API_KEY_WEATHER)

    def onboard_user(self):
        # Collect user details for onboarding
        print("Welcome! Please enter your details.")
        phone_number = input("Enter your phone number: ")
        name = input("Enter your name: ")
        city = input("Enter your city: ")
        postal_code = input("Enter your postal code: ")

        # Register user via SMS provider

        res =  self.SMSService.register_number(int(phone_number))
        if res["status"] =="error":
            print("have error here ")
        print(phone_number)
        self.sms_provider.register_number(int(phone_number))
        print(f"Welcome, {name} from {city} ({postal_code})!")

        # Send an initial SMS asking if they want to receive holiday info
        sms_response = self.SMSService.send_sms(int(phone_number), "Hi, do you want information about the next upcoming holidays? (y/n)")
        if sms_response["status"] =="error":
            print("have error here ")

        # Wait for the response from user
        response = input("Wait for user response (y/n): ").strip().lower()
        if response == "y":
            self.provide_holiday_info(city, postal_code, phone_number)  # Pass phone_number here
        else:
            print("Okay, have a great day!")

    def provide_holiday_info(self, city, postal_code, phone_number):
        # Get the next holiday from NagerHolidayProvider
        holidays = self.holiday_service.get_next365_holidays("DE", phone_number)
        if holidays:
            holiday = holidays[0]
            holiday_name = holiday["name"]
            holiday_date = holiday["date"]

            print(f"The next holiday is {holiday_name} on {holiday_date}.")
            
            # Get weather for that holiday using the WeatherService
            weather_data = self.weather_app.get_weather_data(city, phone_number)

            # Get events using Ticketmaster API
            events = self.event_service.get_local_events(city, phone_number)

            # Prepare the SMS content
            current_weather = weather_data.get('currentConditions', {})
            weather_msg = f"Weather on {holiday_name} in {city}: {current_weather.get('conditions', 'N/A')}, {current_weather.get('temp', 'N/A')}°C"

            event_msg = "Events near you: "
            for event in events[:5]:  # Get the first 5 events
                event_msg += f"{event['name']} on {event['date']} at {event['venue']}. "

            # Combine messages, keeping under the 160 character limit
            message = f"Holiday Info: {holiday_name} ({holiday_date}). {weather_msg} {event_msg}"
            self.send_sms_in_chunks(phone_number, message)  # Now phone_number is defined

    def send_sms_in_chunks(self, phone_number, message):
        # Send SMS in chunks if it's too long
        max_length = 160
        while len(message) > max_length:
            chunk = message[:max_length]
            self.SMSService.send_sms(phone_number, chunk)
            message = message[max_length:]

        # Send remaining message if any
        if message:
            self.SMSService.send_sms(phone_number, message)

# Main function to run the application
def main():
    app = MainApp()
    app.onboard_user()

if __name__ == "__main__":
    main()
