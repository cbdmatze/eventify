
import requests
import json

class EventService:
    """
    Service class for interacting with the Ticketmaster API to fetch local events.
    """

    def __init__(self, api_key: str):
        """
        Initializes the EventService with the given API key.

        Args:
            api_key (str): The API key for Ticketmaster.
        """
        self.api_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        self.api_key = api_key

    def get_local_events(self, city: str):
        """
        Fetches local events from Ticketmaster based on the given city.

        Args:
            city (str): The city for which to fetch events.

        Returns:
            list: A list of event dictionaries with event details, or None on failure.
        """
        params = {
            'apikey': self.api_key,
            'city': city,
            'radius': '100',
            'size': '10'
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            event_data = response.json()
            events = self.extract_event_info(event_data)
            self.save_event_data_to_json(events, 'data/user_data.json')
            return events
        else:
            print(f"Error fetching events: {response.status_code}")
            return None

    def extract_event_info(self, event_data: dict):
        """
        Extracts event information from the API response.

        Args:
            event_data (dict): The raw event data from the Ticketmaster API.

        Returns:
            list: A list of events with relevant details.
        """
        events = []
        if '_embedded' in event_data:
            for event in event_data['_embedded']['events']:
                venue = event['_embedded'].get('venues', [{}])[0]
                events.append({
                    'name': event.get('name', 'Event name not available'),
                    'date': event['dates']['start'].get('localDate', 'Date not available'),
                    'venue': venue.get('name', "Venue not available"),
                    'url': event.get('url', "Link not available")
                })
        return events

    def save_event_data_to_json(self, events: list, filename: str):
        """
        Saves the event data to a JSON file.

        Args:
            events (list): The list of events to save.
            filename (str): The file to save the events to.
        """
        try:
            with open(filename, 'r+') as file:
                data = json.load(file)
                data['events'] = events
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                json.dump({'events': events}, file, indent=4)
