from abc import ABC, abstractmethod

class ISmsProvider(ABC):
    """
    Abstract base class for SMS providers. Defines the required methods for
    implementing an SMS provider.
    """

    @abstractmethod
    def register_number(self, number: int):
        """
        Registers a phone number with the provider.

        Args:
            number (int): The phone number to register.
        """
        pass

    @abstractmethod
    def un_register_number(self, number: int):
        """
        Unregisters a phone number from the provider.

        Args:
            number (int): The phone number to unregister.
        """
        pass

    @abstractmethod
    def send_sms(self, to: str, message: str):
        """
        Sends an SMS to the specified phone number.

        Args:
            to (str): The recipient's phone number.
            message (str): The message content.
        """
        pass

    @abstractmethod
    def get_messages(self):
        """
        Retrieves incoming messages from the provider.
        """
        pass
