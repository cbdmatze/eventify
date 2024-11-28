from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider

class SMSController():
    def __init__(self):
        self.sms_provider = MasterSchoolSMSProvider()

    def get_team_name(self):
        print(self.sms_provider.team_name)

    def add_new_team(self, team_name: str):
        print(self.sms_provider.addNewTeam(team_name))

    def register_number(self, number: str):
        print(self.sms_provider.register_number(number))

    def send_sms(self, number: int, message: str):
        print(self.sms_provider.send_sms(number, message))
