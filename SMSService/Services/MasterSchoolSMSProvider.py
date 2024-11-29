from SMSService.Interface.ISmsProvider import ISmsProvider
import requests

BASE_URL = "http://hackathons.masterschool.com:3030/"
BASE_TEAM_NAME = "TheIdentifiers"

class MasterSchoolSMSProvider(ISmsProvider):
    def un_register_number(self, number: int):
        pass

    def register_number(self, number: int):
        endpoint = "team/registerNumber"
        json_body = {
            "phoneNumber": number,
            "teamName": f"{BASE_TEAM_NAME}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def get_messages(self):
        endpoint = f"team/getMessages/{BASE_TEAM_NAME}"
        return self.call_api("GET", endpoint)

    def send_sms(self, to: int, message: str):
        endpoint = "sms/send"
        json_body ={
            "phoneNumber": to,
            "message": message,
            "sender": ""
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def addNewTeam(self, team_name):
        endpoint = "team/addNewTeam"
        json_body = {
            "teamName": f"{team_name}"
        }
        return self.call_api("POST", endpoint, json_body=json_body)

    def call_api(self, method: str, endpoint: str, json_body=None, query_params=None):
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
