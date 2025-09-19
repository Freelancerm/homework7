from abc import ABC, abstractmethod


# Інтерфейс msgSender
class MessageSender(ABC):
    @abstractmethod
    def send_message(self, msg: str, **kwargs):
        pass


# Існуючі класи для відправки повідомлень
class SMSService:
    @staticmethod
    def send_sms(phone_number: str, msg: str):
        print(f"Відправка SMS на {phone_number}: {msg}")
        return True


class EmailService:
    @staticmethod
    def send_email(email_address: str, msg: str):
        print(f"Відправка Email на {email_address}: {msg}")
        return True


class PushService:
    @staticmethod
    def send_push(device_id: str, msg: str):
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {msg}")
        return True


# Адаптери
class SMSAdapter(MessageSender):
    def __init__(self, _sms_service: SMSService, _phone_number: str):
        self.sms_service = _sms_service
        self.phone_number = _phone_number

    def send_message(self, msg: str, **kwargs):
        try:
            self.sms_service.send_sms(self.phone_number, msg)
            return True
        except Exception as ex:
            print(f"Помилка відавки MS: {ex}")
            return False


class EmailAdapter(MessageSender):
    def __init__(self, _email_service: EmailService, _email_address: str):
        self.email_service = _email_service
        self.email_address = _email_address

    def send_message(self, msg: str, **kwargs):
        try:
            self.email_service.send_email(self.email_address, msg)
            return True
        except Exception as ex:
            print(f"Помилка відправки Email: {ex}")
            return False


class PushAdapter(MessageSender):
    def __init__(self, _push_service: PushService, _device_id: str):
        self.push_service = _push_service
        self.device_id = _device_id

    def send_message(self, msg: str, **kwargs):
        try:
            self.push_service.send_push(self.device_id, msg)
            return True
        except Exception as ex:
            print(f"Помилка відправки Push: {ex}")
            return False


# Система відправки повідомлень
class Messenger:
    def __init__(self, _adapters: list[MessageSender]):
        self.adapters = _adapters

    def send_to_all(self, msg: str):
        print(f"\n--- Відправка через усі доступні сервіси ---")
        for adapter in self.adapters:
            adapter.send_message(msg)
        print("--- Відправка завершена ---\n")


# Використання
sms_service = SMSService()
email_service = EmailService()
push_service = PushService()

sms_adapter = SMSAdapter(sms_service, "+380123456789")
email_adapter = EmailAdapter(email_service, "user@example.com")
push_adapter = PushAdapter(push_service, "device123")

message_text = "Це тестове повідомлення. Привіт!"
print("\n--- Відправка через окремі адаптери ---")
sms_service.send_sms(phone_number="+380123456789", msg=message_text)
email_service.send_email(email_address="user@example.com", msg=message_text)
push_service.send_push(device_id="device123", msg=message_text)

all_senders = Messenger([sms_adapter, email_adapter, push_adapter])
all_senders.send_to_all("Друге текстове повідомлення. Тепер усім!")
