from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider
from EventService import EventService
from HolidayService.Controller.HolidayController import HolidayController
from HolidayService.Services.NagerHolidayProvider import NagerHolidayProvider
from WeatherService import WeatherService
import json
import os
from dotenv import load_dotenv


def load_env_variables():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv()
    return {
        'holiday_api_key': os.getenv("HOLIDAY_API_KEY"),
        'weather_api_key': os.getenv("WEATHER_API_KEY"),
        'ticketmaster_api_key': os.getenv("TICKETMASTER_API_KEY"),
    }


def load_user_data():
    """
    Loads user data from the user_data.json file.
    
    Returns:
        dict: The user data loaded from the file.
    """
    try:
        with open("data/user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("User data file not found, initializing empty data.")
        return {}
    

def save_user_data(user_data):
    """
    Saves user data to the user_data.json file.
    
    Args:
        user_data (dict): The data to save the file.
    """
    with open("data/user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)


def onboard_user(sms_provider, user_phone):
    """
    Onboards a new user by registering their phone number with the SMS provider.
    
    Args:
        sms_provider (MaserSchoolSMSProvider): The SMS provider instance.
        user_phone (str): The user's phone number.
    """
    sms_provider.register_number(user_phone)
    print(f"User with phone number {user_phone} onboarded successfully.")
   

def get_personalized_info(user_data, event_service, holiday_service, weather_service):
    """
    Fetches personalized event, holiday and weather data for the user.
    
    Args:
        user_data (dict): The user-specific data (city, postal code, etc.).
        event_service (EventService): The event service instance.
        holiday_service (HolidayController): The holiday service instance.
        weather_service (WeatherService): The weather service instance.
        
    Returns:
        dict: The combined data of events, holidays, and weather.
    """
    city = user_data.get('city', 'default_city')
    postal_code = user_data.get('postal_code', 'default_postal_code')

    # Get event data
    events = event_service.get_local_events(city)

    # Get holiday data
    try:
        next_holiday = holiday_service.get_next_holidays('DE')
    except Exception as e:
        print(f"Error fetching holidays: {e}")
        next_holiday = None
    
    # Get weather forecast data 
    if next_holiday:
        holiday_date = next_holiday[0]['date']
        forecast = weather_service.get_weather_forecast(postal_code, holiday_date)
    else:
        forecast = None
    
    return {
        'events': events, 
        'holiday': next_holiday, 
        'weather': forecast
    }


def send_personalized_info(sms_provider, user_phone, info):
    """
    Sends personalized information to the user via SMS.
    
    Args:
        sms_provider (MasterSchoolSMSProvider): The SMS provider instance.
        user_phone (str): The user's phone number.
        info (dict): the personalized information to send.
    """
    message = f"Holiday: {info['holiday'][0]['name']} on {info['holiday'][0]['date']}."
    
    if info['events']:
        message += f" Nearby Events: {info['events'][0]['name']} at {info['events'][0]['venue']}."

    if info.get('holiday') and info['holiday'][0].get('name'):
        message = f"Holiday: {info['holiday'][0]['name']} on {info['holiday'][0]['date']}."
    else:
        message = "No upcoming holidays found."

    if info.get('events') and len(info['events']) > 0:
        message += f" Nearby Events: {info['events'][0]['name']} at {info['events'][0]['venue']}."
    else:
        message += " No events found."

    sms_provider.send_sms(user_phone, message)
    print(f"Message sent to {user_phone}: {message}")


def create_html_summary_page(info, user_phone):
    """
    Creates an HTML summary page with the personalized information.
    
    Args:
        info (dict): the personalized information (events, holidays, weather).
        user_phone (str): the user's phone number.
        
    Returns:
        srt: The file path of the generated HTML page.
    """
    html_content = f"""
    <html>
    <head><title>Personalized Info</title></head>
    <body>
        <h1>Holiday Information</h1>
        <p>Next holiday: {info['holiday'][0]['name']} on {info['holiday'][0]['date']}</p>

        <h2>Weather Forecast</h2>
        {"".join([f"<p>{day['date']}: {day['description']} with {day['temp']}°C</p>" for day in info['weather']]) if info['weather'] else '<p>No forecast available</p>'}

        <h2>Upcoming Events</h2>
        {"".join([f"<p>{event['name']} at {event['venue']} on {event['date']}</p>" for event in info['events']]) if info['events'] else '<p>No events found</p>'}
    </body>
    </html>
    """

    file_path = f"data/{user_phone}_summary.html"
    with open(file_path, "w") as file:
        file.write(html_content)
    print(f"HTML summary page created: {file_path}")
    return file_path


def main():
    """
    The main function concerts the orchestra.
    """
    # Load environment variables and the user data
    env_vars = load_env_variables()
    user_data = load_user_data()

    # Initialize Services
    sms_provider = MasterSchoolSMSProvider()
    event_service = EventServic(env_vars['ticketmaster_api_key'])
    holiday_provider = NagerHolidayProvider()
    holiday_service = HolidayController(holiday_provider)
    weather_service = WeatherService(env_vars['weather_api_key'])

    user_phone = user_data.get("phone")

    if not user_phone:
        print("No user phon number found, onboarding a new user.")
        user_phone = input("Please enter your phone number: ")
        onboard_user(sms_provider, user_phone)
        user_data['phone'] = user_phone
        save_user_data(user_data)

    # Fetch personalized user info
    personalized_info = get_personalized_info(user_data, event_service, holiday_service, weather_service)

    # Send personalized info via SMS
    send_personalized_info(sms_provider, user_phone, personalized_info)

    # Create and send HTML summary link
    html_summary_path = create_html_summary_page(personalized_info, user_phone)
    sms_provider.send_sms(user_phone, f"View your personalized summary here: {html_summary_path}")

if __name__ == "__main__":
    main()
