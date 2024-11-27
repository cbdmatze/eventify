from SMSService.Services.MasterSchoolSMSProvider import MasterSchoolSMSProvider

class SMSController:
    """
    Controller for handling SMS-related operations using the MasterSchoolSMSProvider.
    """

    def __init__(self):
        """
        Initializes the SMSController and sets up the SMS provider.
        """
        self.sms_provider = MasterSchoolSMSProvider()

    def send_sms(self, phone_number: int, message: str):
        """
        Sends an SMS to the given phone number.

        Args:
            phone_number (int): The phone number to send the SMS to.
            message (str): The message content to send.

        Returns:
            dict: The response from the SMS provider.
        """
        response = self.sms_provider.send_sms(phone_number, message)
        return response

    def register_number(self, phone_number: str):
        """
        Registers a phone number with the SMS provider.

        Args:
            phone_number (str): The phone number to register.

        Returns:
            dict: The response from the SMS provider.
        """
        response = self.sms_provider.register_number(phone_number)
        return response
