"""
Скрипт що демонструє використання патерну проектування 'Адаптер'
для уніфікації інтерфейсів різних сервісів відправки повідомлень
(SMS, Email, Push).
"""

from abc import ABC, abstractmethod


# Інтерфейс (абстрактний базовий клас) для відправника повідомлень
class MessageSender(ABC):
    @abstractmethod
    def send_message(self, msg: str, **kwargs):
        """ Абстрактний метод для відправки повідомлення. """
        pass


# Існуючі класи для відправки повідомлень
class SMSService:
    @staticmethod
    def send_sms(phone_number: str, msg: str):
        """ Відправляє SMS-повідомлення. """
        print(f"Відправка SMS на {phone_number}: {msg}")
        return True


class EmailService:
    @staticmethod
    def send_email(email_address: str, msg: str):
        """ Відправляє Email-повідомлення. """
        print(f"Відправка Email на {email_address}: {msg}")
        return True


class PushService:
    @staticmethod
    def send_push(device_id: str, msg: str):
        """ Відправляє Push-повідомлення. """
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {msg}")
        return True


# Класи-адаптери, які обгортають існуючі сервіси та реалізують єдиний інтерфейс MessageSender
class SMSAdapter(MessageSender):
    def __init__(self, _sms_service: SMSService, _phone_number: str):
        """ Метод-ініціалізатор """
        self.sms_service = _sms_service
        self.phone_number = _phone_number

    def send_message(self, msg: str, **kwargs):
        """ Адаптований метод для відправки SMS. """
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
        """ Адаптований метод для відправки Email. """
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
        """ Адаптований метод для відправки Push. """
        try:
            self.push_service.send_push(self.device_id, msg)
            return True
        except Exception as ex:
            print(f"Помилка відправки Push: {ex}")
            return False


# Система відправки повідомлень
class Messenger:
    def __init__(self, _adapters: list[MessageSender]):
        """ Ініціалізує месенджер зі списком адаптерів. """
        self.adapters = _adapters

    def send_to_all(self, msg: str):
        """ Відправляє повідомлення через усі доступні адаптери. """
        print(f"\n--- Відправка через усі доступні сервіси ---")
        for adapter in self.adapters:
            adapter.send_message(msg)
        print("--- Відправка завершена ---\n")


# Використання: створюємо сервіси, адаптери, і демонструємо їх роботу
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

# Використання класу-агрегатора, який працює з уніфікованими адаптерами
all_senders = Messenger([sms_adapter, email_adapter, push_adapter])
all_senders.send_to_all("Друге текстове повідомлення. Тепер усім!")
