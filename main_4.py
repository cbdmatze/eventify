from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider
from EventService import EventService
from HolidayService.Controller.HolidayController import HolidayController
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from WeatherService import WeatherService
import json
import os
# from dotenv import load_dotenv
from datetime import datetime, timezone, time

USER_DATA_PATH = 'data/user_data.json'


def load_env_vars():
    """Load environment variables from the .env file."""
    #load_dotenv()
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
    """Onboard a new user by collecting their phone number, postal code, and city."""
    postal_code = input("Please enter your postal code: ")
    city = input("Please enter your city: ")

    # Store user data (phone number, postal code, and city)
    user_data = {
        "phone_number": phone_number,
        "postal_code": postal_code,
        "city": city,
        "events": []  # Add events as an empty list initially
    }

    # Save user data to 'user_data.json'
    save_user_data(user_data)

    print(f"User with phone number {phone_number} onboarded successfully.")


def get_personalized_info(postal_code, city):
    """Fetch personalized information like weather, events, and holidays."""
    # Initialize services with API keys from env_vars
    weather_service = WeatherService(api_key='HLU729E56SMY3M2FCQJLCXEYM')
    event_service = EventService(api_key='8yHnQv1827D9Gtj6HhnmDIqLBU2zB4CA')
    holiday_provider = NagerHolidayProvider()
    holiday_controller = HolidayController(provider=holiday_provider)

    # Fetch weather information with error handling
    try:
        weather_info = weather_service.get_weather(postal_code)
        
        if weather_info is None:
           weather_info = {'list': []}  
            #raise ValueError("Failed to fetch weather data. Please check your API key or postal code.")
    except Exception as e:
        print(f"Error fetching weather data: {e}")
         # Return an empty weather list on error
        # Log additional details for debugging
        #print(f"Weather API Error for postal code {postal_code}: {e}")

    # Fetch events for the city
    try:
        events = event_service.get_local_events(city)
        if not events:
            print("No events data available.")
    except Exception as e:
        print(f"Error fetching events data: {e}")
        events = []  # Return an empty events list on error
        # Log additional details for debugging
        print(f"Event API Error for city {city}: {e}")

    # Fetch upcoming holidays
    try:
        holidays = holiday_controller.get_next365_holidays("DE")
    except Exception as e:
        print(f"Error fetching holidays: {e}")
        holidays = []

    # Now handle the 'weather_info' as a list
    personalized_info = {
        "weather": weather_info[:5],  # Take the next 5 days if it's a list
        "events": events,
        "holiday": holidays[:1]  # Get the next upcoming holiday
    }
    
    return personalized_info


def update_user_events(user_data, events):
    """Update the user data with new events."""
    user_data['events'] = events
    save_user_data(user_data)


def send_personalized_info(personalized_info, phone_number):
    """Send personalized info to the user via SMS."""
    if personalized_info['holiday']:
        holiday_info = personalized_info['holiday'][0]
        message = f"Holiday: {holiday_info['name']} on {holiday_info['date']}."
    else:
        message = "No upcoming holidays found."

    # Initialize MasterSchoolSMSProvider
    sms_provider = MasterSchoolSMSProvider()
    try:
        # Send the SMS to the phone number
        sms_provider.send_sms(phone_number, message)
        print(f"Message sent to {phone_number}: {message}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


def main():
    # Load environment variables
    env_vars = load_env_vars()

    # Load existing user data
    user_data = load_user_data()

    # Onboard the user if no data is found
    if not user_data:
        phone_number = input("Please enter your phone number: ")
        onboard_user(phone_number)
        user_data = load_user_data()  # Refresh user data after onboarding

    # Get postal code and city from user data
    postal_code = user_data.get("postal_code")
    city = user_data.get("city")

    # Fetch personalized info (including events and weather) using the postal code and city
    personalized_info = get_personalized_info(postal_code, city)

    # Update the user data with the fetched events
    update_user_events(user_data, personalized_info['events'])

    # Send personalized info to the user via SMS
    send_personalized_info(personalized_info, user_data['phone_number'])

    # Create an HTML summary page
    #html_summary_path = create_html_summary_page(personalized_info, user_data['phone_number'])
    #print(f"HTML summary page created at: {html_summary_path}")


if __name__ == "__main__":
    main()
