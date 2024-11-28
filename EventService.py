import requests
import json

class EventService:
    def __init__(self, api_key):
        self.api_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        self.api_key = api_key

    def get_local_events(self, city, user_phone):
        params = {
            'apikey': self.api_key,
            'city': city,
            'radius': '100',
            'size': '5'
        }

        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            event_data = response.json()
            events = self.extract_event_info(event_data)
            self.save_user_data(user_phone, {'events': events})
            return events
        else:
            print(f"Error fetching events: {response.status_code}")
            return None

    def extract_event_info(self, event_data):
        events = []
        if '_embedded' in event_data:
            for event in event_data['_embedded']['events']:
                venue = event['_embedded'].get('venues', [{}])[0]
                venue_name = venue.get('name', "Venue not available")
                event_url = event.get('url', "Link not available")

                events.append({
                    'name': event.get('name', 'Event name not available'),
                    'date': event['dates']['start'].get('localDate', 'Date not available'),
                    'venue': venue_name,
                    'url': event_url
                })
        return events

    def save_user_data(self, user_phone, data):
        try:
            # Load existing data
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}

        # Update user data with new data
        if user_phone not in user_data:
            user_data[user_phone] = {}
        
        user_data[user_phone].update(data)

        # Save back to user_data.json
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
