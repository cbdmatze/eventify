from abc import ABC, abstractmethod

class ISmsProvider(ABC):

    @abstractmethod
    def register_number(self, number: int):
        pass

    @abstractmethod
    def un_register_number(self, number: int):
        pass

    @abstractmethod
    def send_sms(self, to: str, message: str):
        pass

    @abstractmethod
    def get_messages(self, number: int):
        pass