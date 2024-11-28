from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider
from EventService import EventService
from HolidayService.Controller.HolidayController import HolidayController
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from WeatherService import WeatherService
import json
import os
from datetime import datetime

USER_DATA_PATH = 'data/user_data.json'


def load_env_vars():
    """Load environment variables from the .env file."""
    return {
        'weather_api_key': os.getenv("VISUALCROSSING_API_KEY"),
        'ticketmaster_api_key': os.getenv("TICKETMASTER_API_KEY"),
    }


def load_user_data():
    """Retrieve user data from the JSON file."""
    if os.path.exists(USER_DATA_PATH):
        try:
            with open(USER_DATA_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
    return {}


def save_user_data(user_data):
    """Save user data to the JSON file."""
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(user_data, f, indent=4)


def onboard_user(phone_number):
    """Onboard a new user by collecting and saving their information."""
    user_data = load_user_data()
    if phone_number in user_data:
        print(f"User {phone_number} is already onboarded.")
        return

    # Ask for user's details and add to user_data
    user_data[phone_number] = {
        'name': input("Enter your name: "),
        'birthday': input("Enter your birthday (YYYY-MM-DD): "),
        'city': input("Enter your city: "),
        'postal_code': input("Enter your postal code: ")
    }

    save_user_data(user_data)
    print(f"User {phone_number} has been onboarded.")


def send_personalized_info(phone_number, user_data):
    """Send personalized information to the user via SMS."""
    event_service = EventService(os.getenv("TICKETMASTER_API_KEY"))
    weather_service = WeatherService(os.getenv("VISUALCROSSING_API_KEY"))
    holiday_service = HolidayController(NagerHolidayProvider())

    events = event_service.get_local_events(city=user_data['city'])
    weather = weather_service.get_weather(city=user_data['city'])
    holidays = holiday_service.get_holidays()

    # Create personalized message
    message = f"Upcoming holiday: {holidays[0]['name']} on {holidays[0]['date']}\n"
    message += f"Weather forecast for {user_data['city']}:\n"
    for day in weather:
        message += f"{day['date']}: {day['temp']}°C, {day['description']}\n"
    message += f"Nearby events: {events[0]['name']} at {events[0]['venue']}"

    # Send the SMS (example, replace with actual SMS sending code)
    print(f"Sending message to {phone_number}: {message}")


def main():
    phone_number = input("Enter your phone number: ")
    onboard_user(phone_number)
    user_data = load_user_data().get(phone_number, {})
    send_personalized_info(phone_number, user_data)


if __name__ == '__main__':
    main()
