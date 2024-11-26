import requests
import json

class EventService:
    def __init__(self, api_key):
        self.api_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        self.api_key = api_key

    def get_local_events(self, city):
        """
        Fetch events happening near the given city and store the response in a file.
        """
        params = {
            'apikey': self.api_key,
            'city': city,       # Pass the city dynamically
            'radius': '100',    # Search radius in kilometers
            'size': '10'        # Limit the number of events returned
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            event_data = response.json()
            self.save_event_data_to_file(event_data)  # Save response to file
            return self.extract_event_info(event_data)
        else:
            print(f"Error fetching events: {response.status_code}")
            return None

    def extract_event_info(self, event_data):
        """
        Extract and format the event information for SMS notification.
        """
        events = []
        if '_embedded' in event_data:
            for event in event_data['_embedded']['events']:
                # Safely get venue information if it exists
                venue = event['_embedded'].get('venues', [{}])[0]
                venue_name = venue.get('name', "Venue not available")
                
                # Safely get event URL
                event_url = event.get('url', "Link not available")

                events.append({
                    'name': event.get('name', 'Event name not available'),
                    'date': event['dates']['start'].get('localDate', 'Date not available'),
                    'venue': venue_name,
                    'url': event_url
                })
        return events

    def save_event_data_to_file(self, event_data):
        """
        Save the raw event data to a file called 'events_data.json'.
        """
        try:
            with open('events_data.json', 'w') as file:
                json.dump(event_data, file, indent=4)
            print("Event data saved to 'events_data.json'.")
        except IOError as e:
            print(f"Error saving event data to file: {e}")


if __name__ == "__main__":
    api_key = "8yHnQv1827D9Gtj6HhnmDIqLBU2zB4CA"  
    city = "Berlin"  # Example city
    
    event_service = EventService(api_key)
    events = event_service.get_local_events(city)

    if events:
        for event in events:
            print(f"Event: {event['name']}\nDate: {event['date']}\nVenue: {event['venue']}\nLink: {event['url']}\n")
    else:
        print("No events found.")
