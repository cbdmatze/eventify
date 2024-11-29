from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider
from EventService import EventService
from HolidayService.Controller.HolidayController import HolidayController
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from WeatherService import WeatherService
import json
import os
from dotenv import load_dotenv
from datetime import datetime


USER_DATA_PATH = 'data/user_data.json'


def get_user_data():
    """Retrieve user data from the JSON file."""
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as f:
            return json.load(f)
    return {}

def onboard_user(phone_number):
    """Onboard a new user by collecting their phone number and postal code."""
    # Ask for the user's postal code if not available
    postal_code = input("Please enter your postal code: ")
    
    # Store user data (phone number and postal code)
    user_data = {
        "phone_number": phone_number,
        "postal_code": postal_code
    }
    
    # Save user data to 'user_data.json'
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(user_data, f)
    
    print(f"User with phone number {phone_number} onboarded successfully.")

def get_personalized_info(postal_code):
    """Fetch personalized information like weather, events, and holidays."""
    # Initialize services (use your actual API keys here)
    weather_service = WeatherService(api_key="YOUR_WEATHER_API_KEY")
    event_service = EventService(api_key="YOUR_EVENT_API_KEY")
    holiday_provider = NagerHolidayProvider()
    holiday_controller = HolidayController(provider=holiday_provider)
    
    # Fetch weather information
    weather_info = weather_service.get_weather_by_postal_code(postal_code)
    
    # Fetch events
    events = event_service.get_events_near_postal_code(postal_code)
    
    # Fetch upcoming holidays
    try:
        holidays = holiday_controller.get_next365_holidays("DE")
    except Exception as e:
        print(f"Error fetching holidays: {e}")
        holidays = []

    # Build the personalized information dictionary
    personalized_info = {
        "weather": weather_info.get('list', [])[:5],  # Take the next 5 days
        "events": events,
        "holiday": holidays[:1]  # Get the next upcoming holiday
    }

    return personalized_info

def send_personalized_info(personalized_info, phone_number):
    """Send personalized info to the user (for example, as an SMS)."""
    # Here you would integrate with your SMS provider
    if personalized_info['holiday']:
        holiday_info = personalized_info['holiday'][0]
        message = f"Holiday: {holiday_info['name']} on {holiday_info['date']}."
    else:
        message = "No upcoming holidays found."
    
    # Send the message (this part would need to integrate with your SMS system)
    print(f"Message sent to {phone_number}: {message}")

def create_html_summary_page(personalized_info, phone_number):
    """Create an HTML summary page from the personalized info."""
    html_content = f"""
    <html>
    <head><title>Personalized Info for {phone_number}</title></head>
    <body>
    <h1>Personalized Information for {phone_number}</h1>
    <h2>Weather Forecast</h2>
    <ul>
    """
    
    for weather in personalized_info['weather']:
        date = datetime.utcfromtimestamp(weather['dt']).strftime('%Y-%m-%d')
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        html_content += f"<li>{date}: {temp}°C, {description}</li>"
    
    html_content += """
    </ul>
    <h2>Upcoming Events</h2>
    <ul>
    """
    
    for event in personalized_info['events']:
        event_name = event['name']
        event_date = event['dates']['start']['localDate']
        html_content += f"<li>{event_name} on {event_date}</li>"
    
    html_content += """
    </ul>
    <h2>Next Holiday</h2>
    """
    
    if personalized_info['holiday']:
        holiday = personalized_info['holiday'][0]
        holiday_name = holiday['name']
        holiday_date = holiday['date']
        html_content += f"<p>{holiday_name} on {holiday_date}</p>"
    else:
        html_content += "<p>No upcoming holidays found.</p>"
    
    html_content += """
    </body>
    </html>
    """
    
    # Save the HTML content to a file
    file_path = f"data/summary_{phone_number}.html"
    with open(file_path, 'w') as f:
        f.write(html_content)
    
    return file_path

def main():
    user_data = get_user_data()
    
    if not user_data:
        phone_number = input("Please enter your phone number: ")
        onboard_user(phone_number)
        user_data = get_user_data()  # Refresh user data after onboarding
    
    # Now the user data contains the postal code, which is needed for fetching weather and events
    postal_code = user_data.get("postal_code")
    
    # Fetch personalized info (including events and weather) using the postal code
    personalized_info = get_personalized_info(postal_code)
    
    # Send personalized info to the user
    send_personalized_info(personalized_info, user_data['phone_number'])
    
    # Create an HTML summary page
    html_summary_path = create_html_summary_page(personalized_info, user_data['phone_number'])
    print(f"HTML summary page created at: {html_summary_path}")

if __name__ == "__main__":
    main()
