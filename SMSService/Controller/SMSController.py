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



def main():
    sms_controller = SMSController()
    sms_controller.get_team_name()
    #sms_controller.register_number("015566209074")
    sms_controller.send_sms(15566209074, "Hello, this is a test message!")
   #sms_controller.add_new_team("TeamBBBBBWW")


if __name__ == "__main__":
    main()
