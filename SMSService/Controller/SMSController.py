from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider


class SMSController():
    def __init__(self):
        self.sms_provider = MasterSchoolSMSProvider()

    def get_team_name(self):
        print(self.sms_provider.team_name)

    def add_new_team(self, team_name):
        print(self.sms_provider.addNewTeam(team_name))


def main():
    sms_controller = SMSController()
    sms_controller.get_team_name()
    sms_controller.add_new_team("TeamBBBBBWW")


if __name__ == "__main__":
    main()
