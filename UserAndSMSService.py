import json
import requests

class UserAndSMSService:
    def __init__(self, base_url, data_file='data/user_data.json'):
        self.base_url = base_url
        self.data_file = data_file

    def onboard_and_notify_user(self):
        # Step 1: Onboard the user
        user_data = self.onboard_user()

        # Step 2: Register the team and user phone number
        team_name = input("Enter your team name: ")
        self.register_team(team_name)
        self.register_number(user_data['phone_number'], team_name)

        # Step 3: Send a welcome SMS 
        self.send_sms(user_data['phone_number'], "Welcome to the Hackathon!")
    
        # self.send_weather_update(user_data['phone_number'], weather_data)
        # self.send_event_notification(user_data['phone_number'], events_data)
        # self.send_holiday_notification(user_data['phone_number'], holidays_data)

        return user_data

    def onboard_user(self):
        """
        Collects user details through input prompts and returns the user data.
        """
        name = input("Enter your name: ")
        birthday = input("Enter your birthday: ")
        city = input("Enter your city: ")
        postal_code = input("Enter your postal code: ")
        phone_number = input("Enter your phone number: ")

        user_data = {
            'name': name,
            'birthday': birthday,
            'city': city,
            'postal_code': postal_code,
            'phone_number': phone_number
        }

        # Save the user data to file
        self.save_user_data(user_data)
        return user_data

    def save_user_data(self, user_data):
        """
        Saves the user data to a JSON file.
        """
        with open(self.data_file, 'w') as f:
            json.dump(user_data, f)

    def retrieve_user_data(self):
        """
        Retrieves the user data from a JSON file.
        """
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return None

    def register_team(self, team_name):
        """
        Registers a new team using the Masterschool SMS Hackathon API.
        """
        url = f"{self.base_url}/team/addNewTeam"
        payload = {'teamName': team_name}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(f"Team '{team_name}' registered successfully.")
            return response.json()
        else:
            print(f"Failed to register team '{team_name}'.")
            return None

    def register_number(self, phone_number, team_name):
        """
        Registers the user's phone number to the specified team.
        """
        url = f"{self.base_url}/team/registerNumber"
        payload = {
            'phoneNumber': phone_number,
            'teamName': team_name
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(f"Phone number {phone_number} registered successfully to team '{team_name}'.")
            return response.json()
        else:
            print(f"Failed to register phone number {phone_number}.")
            return None

    def send_sms(self, phone_number, message):
        """
        Sends an SMS to the user via the Masterschool SMS Hackathon API.
        """
        url = f"{self.base_url}/sms/send"
        payload = {
            'phoneNumber': phone_number,
            'message': message,
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(f"SMS sent to {phone_number}: {message}")
            return response.json()
        else:
            print(f"Failed to send SMS to {phone_number}.")
            return None

    def send_weather_update(self, phone_number, weather):
        """
        Sends a weather update via SMS.
        """
        message = f"Weather Update for {weather['city']}:\n"
        message += f"{weather['description']} with a temperature of {weather['temperature']}°C"
        self.send_sms(phone_number, message)

    def send_event_notification(self, phone_number, events):
        """
        Sends event notifications via SMS.
        """
        message = "Upcoming Events:\n"
        for event in events:
            message += f"{event['name']} at {event['venue']} on {event['date']}\n"
        self.send_sms(phone_number, message)

    def send_holiday_notification(self, phone_number, holidays):
        """
        Sends holiday notifications via SMS.
        """
        message = "Upcoming Holidays:\n"
        for holiday in holidays:
            message += f"{holiday['name']} on {holiday['date']}\n"
        self.send_sms(phone_number, message)


if __name__ == "__main__":
    base_url = "http://hackathons.masterschool.com:3030/"
    user_sms_service = UserAndSMSService(base_url)
    user_sms_service.onboard_and_notify_user()
