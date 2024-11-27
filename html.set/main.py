import os
import json
from flask import Flask, render_template
from datetime import datetime
from WeatherService import WeatherService
from EventService import EventService
from HolidayService import HolidayService


app = Flask(__name__)

# API keys (later from .env)
HOLIDAY_API_KEY = '4a7afdb5-2de7-4c6d-90d0-2038b050b9f6'
TICKETMASTER_API_KEY = '8yHnQv1827D9Gtj6HhnmDIqLBU2zB4CA'
VISUALCROSSING_API_KEY = '6R6EZ6N2WTV4PX5JXP84SJQX4'

# Data directories
HTML_DIR = 'html_summaries'
EVENTS_DATA_FILE = 'data/events_data.json'
WEATHER_DATA_FILE = 'data/weather_data.json'
HOLIDAYS_DATA_FILE = 'data/holiday_data.json'


@app.route('/summary/<user_id>')
def display_summary(user_id):
    """
    Route to display the user-specific summary page.
    """
    html_file_path = os.path.join(HTML_DIR, f'{user_id}_summary.html')
    if os.path.exists(html_file_path):
        return render_template(f'{user_id}_summary.html')
    else:
        return "Summary not available", 404
    

def create_summary_html(user_id, city, postal_code):
    """
    Function to fetch data form the APIs, generate the HTML summary, and save it.
    """
    # Fetch weather data
    weather_service = WeatherService(VISUALCROSSING_API_KEY)
    weather_service.fetch_and_save_weather(city, WEATHER_DATA_FILE)

    # Fetch event data
    event_service = EventService(TICKETMASTER_API_KEY)
    events = event_service.get_local_events(city)

    # Fetch holiday data
    holiday_service = HolidayService(HOLIDAY_API_KEY)
    holidays = holiday_service.get_holidays('DE', datetime.now().year)
    upcoming_holiday = holiday_service.get_upcoming_holiday(holidays)

    # Generate HTML content
    html_content = generate_html_content(events, weather_app, upcoming_holiday)
    
    # Save the HTML to file
    html_file_path = os.path.join(HTML_DIR, f'{user_id}_summary.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Summary HTML created for user {user_id}")


def generate_html_content(events, weather_data, upcoming_holiday):
    """
    Generate the HTML content from event, weather, and holiday data.
    """
    holiday_name, holiday_date = upcoming_holiday if upcoming_holiday else ("No upcoming holiday", "N/A")
    weather_html = f"""
    <h2>Upcoming Holiday: {holiday_name} on {holiday_date}</h2>
    <h3>Weather Forecast:</h3>
    <ul>
        {"".join([f"<li>{day['datetime']}: {day['conditions']} - {day['temp']}°C</li>" for day in weather_data['days']])}
    </ul>
    """

    events_html = "<h3>Nearby Events:</h3><ul>"
    for event in events:
        events_html += f"<li>{event['name']} on {event['date']} at {event['venue']} - <a href='{event['url']}'>Book Now</a></li>"
    events_html += "</ul>"

    return f"""
    <html>
    <head><title>User Summary</title></head>
    <body>
    <h1>Your Personalized Summary</h1>
    {weather_html}
    {events_html}
    </body>
    </html>
    """


def cleanup_old_files():
    """
    Removie HTML files that are older than 30 days to save disk space.
    """
    now = datetime.now().timestam()
    for file in os.listdir(HTML_DIR):
        file_path = os.path.join(HTML_DIR, file)
        if os.path.isfile(file_path):
            file_age = now - os.path.getctime(file_path)
            if file_age > 30 * 24 * 60 * 60:  # 30 days in seconds
                os.remove(file_path)
                print(f"Deleted old summary: {file}")


if __name__ == "__main__":
    # Start the Flask server
    app.run(host='0.0.0.0', port=5001)
    
    # Cleanup old HTML files at intervals (set this up as a scheduled job)
    cleanup_old_files()
