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
        # Convert the timestamp to UTC
        todays_time = datetime.now()
        date = datetime.fromtimestamp(todays_time).date() #fromtimestamp(weather['de'], tz=timezone.utc).strftime('%Y-%m-%d')
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
        event_date = event['date']['start']['localDate']
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