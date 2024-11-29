import threading
import time

from SMSService.Services.Logger import Logger
from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider


class SMSController():
    def __init__(self):
        self.sms_provider = MasterSchoolSMSProvider()
        self.logger = Logger()

    def get_team_name(self):
        return (self.sms_provider.team_name)

    def add_new_team(self, team_name: str):
        return (self.sms_provider.addNewTeam(team_name))

    def register_number(self, number: str):
        return (self.sms_provider.register_number(number))

    def send_sms(self, number: int, message: str):
        return (self.sms_provider.send_sms(number, message))

    def get_all_messages(self):
        res = self.sms_provider.get_messages()
        messages = res["body"]
        self.logger.log_messages(messages)

    def get_last_message(self, phone_number: int):
       # return self.logger.get_last_message(str(phone_number))
        return self.logger.get_last_20ـmessage(str(phone_number),checkTime=4)

    def start_logging_messages(self, interval=600):
        def log_task():
            while True:
                print("Fetching messages...")
                try:
                    messages = self.sms_provider.get_messages()["body"]
                    self.logger.log_messages(messages)
                except Exception as e:
                    print(f"Error while fetching or logging messages: {e}")
                time.sleep(interval)

        thread = threading.Thread(target=log_task, daemon=True)
        thread.start()

    def reload_messages(self,interval=600):
        self.get_all_messages()
        time.sleep(interval)

    def is_more_than_20_minutes(self, createAt):
        self.logger.is_les_than_deatTime_in_cet(createAt)