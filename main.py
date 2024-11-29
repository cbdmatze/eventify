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
        self.register_number(int(phone_number))

        # Send an initial SMS asking if they want to receive holiday info
        self.send_guid_sms(int(phone_number))

        # Wait for the response from user
        if self.waiting_for_response(int(phone_number)):
            self.provide_holiday_info(city, postal_code, phone_number)  # Pass phone_number here
        else:
            print("Okay, have a great day!")
            exit()

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


    def waiting_for_response(self, phone_number: int):
       # return True
        # return self.get_respone_with_terminal();
      return self.is_user_accpet(phone_number)

    def is_user_accpet(self, phone_number: int):
        last_message = self.get_last_message(phone_number)
        if "text" in last_message and (last_message["text"].lower() == "y"):
            return True
        return False



    def get_last_message(self, phone_number):
        result = self.SMSService.get_last_message(phone_number)
        if result["status"] == "error":
            self.SMSService.reload_messages(50)
            self.get_last_message(phone_number)
        else:
            return result["last_message"]

    def get_respone_with_terminal(self):
        response = input("Wait for user response (y/n): ").strip().lower()
        if response == "y":
            return True
        else:
            return False

    def register_number(self, phone_number :int):
        res = self.SMSService.register_number(phone_number)
        if res["status"] == "error":
            print(f"There is some problem in SMS provider : {res['message']}")
            exit()
        return True

    def send_guid_sms(self, phone_number):
        sms_response = self.SMSService.send_sms(int(phone_number),"Hi, do you want information about the next upcoming holidays? (y/n)")
        if sms_response["status"] == "error":
            print(f"There is some problem in SMS provider : {sms_response['message']}")
            exit()
        return True



# Main function to run the application
def main():
    try:
        app = MainApp()
        app.onboard_user()
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")






if __name__ == "__main__":
    main()
