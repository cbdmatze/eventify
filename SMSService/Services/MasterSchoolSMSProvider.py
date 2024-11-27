from SMSService.Interface.ISmsProvider import ISmsProvider
import requests

BASE_URL = "http://hackathons.masterschool.com:3030/"
BASE_TEAM_NAME = "Eventify"


class MasterSchoolSMSProvider(ISmsProvider):
    def un_register_number(self, number: str):
        """
        Unregister a phone number from the service.
        This method sends a request to unregister the provided phone number.

        Args:
            number (str): The phone number to unregister.

        Returns:
            dict: A dictionary containing the status and response message.
        """
        endpoint = "team/unregisterNumber"
        json_body = {
            "phoneNumber": number,
            "teamName": f"{BASE_TEAM_NAME}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def register_number(self, number: str):
        """
        Register a phone number with the service.
        This method sends a request to register the provided phone number.

        Args:
            number (str): The phone number to register.

        Returns:
            dict: A dictionary containing the status and response message.
        """
        endpoint = "team/registerNumber"
        json_body = {
            "phoneNumber": number,
            "teamName": f"{BASE_TEAM_NAME}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def get_messages(self):
        """
        Retrieve all messages from the SMS service.
        This method sends a request to get the list of messages.

        Returns:
            dict: A dictionary containing the status and the list of messages.
        """
        endpoint = "sms/getMessages"
        return self.call_api("GET", endpoint)

    def send_sms(self, to: int, message: str):
        """
        Send an SMS to the specified phone number.

        Args:
            to (int): The phone number to send the SMS to.
            message (str): The content of the SMS to send.

        Returns:
            dict: A dictionary containing the status and response message.
        """
        endpoint = "sms/send"
        json_body = {
            "phoneNumber": to,
            "message": message,
            "sender": f"{BASE_TEAM_NAME}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def addNewTeam(self, team_name: str):
        """
        Add a new team to the system.

        Args:
            team_name (str): The name of the new team.

        Returns:
            dict: A dictionary containing the status and response message.
        """
        endpoint = "team/addNewTeam"
        json_body = {
            "teamName": f"{team_name}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def call_api(self, method: str, endpoint: str, json_body=None, query_params=None):
        """
        Makes a request to the API.

        Args:
            method (str): The HTTP method ('GET' or 'POST').
            endpoint (str): The API endpoint to call.
            json_body (dict, optional): The JSON body for POST requests.
            query_params (dict, optional): The query parameters for GET requests.

        Returns:
            dict: A dictionary containing the status and response from the API.
        """
        headers = {'Content-Type': 'application/json'}
        api_url = f"{BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(api_url, headers=headers, params=query_params)
            elif method == "POST":
                response = requests.post(api_url, headers=headers, json=json_body)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            if "application/json" in response.headers["Content-Type"]:
                return {"status": "success", "message": "Request successful", "body": response.json()}
            else:
                return {"status": "success", "message": "Request successful", "body": response.text}

        except requests.exceptions.HTTPError as e:
            return {"status": "error", "message": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

    @property
    def team_name(self):
        return BASE_TEAM_NAME
