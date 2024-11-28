
from datetime import datetime, timedelta  # Import datetime and timedelta

def create_summary_html(holiday, weather_data, events, user_id):
    # Prepare the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Summary for {user_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            h2 {{
                color: #007bff;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
        </style>
    </head>
    <body>
        <h1>Your Personalized Summary</h1>

        <div class="section">
            <h2>Next Upcoming Holiday</h2>
            <p>{holiday['name']} on {holiday['date']}</p>
        </div>

        <div class="section">
            <h2>Weather Forecast (starting {holiday['date']})</h2>
            <ul>
    """
    
    # Assuming weather_data contains forecast data starting from the holiday date
    holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()  # Use datetime here
    for i in range(7):  # 7-day forecast
        forecast_date = holiday_date + timedelta(days=i)
        forecast = weather_data['days'][i]  # Modify based on your actual data structure
        html_content += f"""
            <li>{forecast_date}: {forecast['conditions']} - {forecast['temp']}°C</li>
        """
    
    html_content += """
            </ul>
        </div>

        <div class="section">
            <h2>Upcoming Events</h2>
            <ul>
    """
    
    # Loop through the events and add them to the HTML
    for event in events:
        html_content += f"""
            <li>
                <strong>{event['name']}</strong><br>
                Date: {event['date']}<br>
                Venue: {event['venue']}<br>
                <a href="{event['url']}" target="_blank">More Info & Book</a>
            </li>
        """

    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """

    # Save the HTML content to a file
    file_name = f"user_summary_{user_id}.html"
    output_dir = "html_summaries"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(os.path.join(output_dir, file_name), 'w') as file:
        file.write(html_content)
    
    return os.path.join(output_dir, file_name)
