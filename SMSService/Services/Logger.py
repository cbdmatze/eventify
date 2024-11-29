import os
import json
from datetime import datetime, timedelta

import pytz
from dateutil.parser import isoparse


class Logger:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if self.file_path is None:
            self.set_default_path()

    def set_default_path(self):
        sms_service_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        storage_dir = os.path.join(sms_service_dir, "Storage")
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        self.file_path = os.path.join(storage_dir, "messages_log.json")


    def log_messages(self, messages):
        try:
            current_data = {}
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                with open(self.file_path, "r") as f:
                    current_data = json.load(f)

            if isinstance(messages, list):
                messages_dict = {}
                for item in messages:
                    messages_dict.update(item)
            else:
                messages_dict = messages

            for number, new_messages in messages_dict.items():
                if number not in current_data:
                    current_data[number] = []

                existing_messages = {msg["receivedAt"]: msg for msg in current_data[number]}
                for message in new_messages:
                    # اصلاح فرمت تاریخ برای سازگاری با datetime.fromisoformat
                    message["receivedAt"] = message["receivedAt"].replace("+0000", "+00:00")
                    if message["receivedAt"] not in existing_messages:
                        current_data[number].append(message)

                current_data[number] = sorted(
                    current_data[number],
                    key=lambda x: datetime.fromisoformat(x["receivedAt"])
                )

            with open(self.file_path, "w") as f:
                json.dump(current_data, f, indent=4)
            print(f"Checking new messages")
            print(f"Messages logged successfully to {self.file_path}")

        except json.JSONDecodeError:
            print("Error: JSON file is corrupted or empty.")
        except Exception as e:
            print(f"Error while logging messages: {e}")

    def get_last_message(self, phone_number):
        try:
            with open(self.file_path, "r") as f:
                current_data = json.load(f)

            if phone_number not in current_data:
                return {"status": "error", "message": "Phone number not found"}

            messages = current_data[phone_number]
            if messages:
                return {"status": "success", "last_message": messages[-1]}  # آخرین پیام
            else:
                return {"status": "error", "message": "No messages found for this number"}

        except FileNotFoundError:
            return {"status": "error", "message": "Message log file not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def get_last_20ـmessage(self, phone_number , checkTime=20):
        try:
            with open(self.file_path, "r") as f:
                current_data = json.load(f)

            if phone_number not in current_data:
                return {"status": "error", "message": "Phone number not found"}

            messages = current_data[phone_number]
            if not messages:
                return {"status": "error", "message": "No messages found for this number"}

            recent_messages = [
                message for message in messages
                if self.is_les_than_deatTime_in_cet(message["receivedAt"], checkTime=checkTime)
            ]

            if recent_messages:
                return {"status": "success", "last_message": recent_messages[-1]}
            else:
                return {"status": "error", "message": "No recent messages in the last 20 minutes"}

        except FileNotFoundError:
            return {"status": "error", "message": "Message log file not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def is_les_than_deatTime_in_cet(self, received_at, checkTime=20):
        try:
            received_time = isoparse(received_at)

            cet = pytz.timezone('CET')
            received_time_cet = received_time.astimezone(cet)

            now_cet = datetime.now(cet)
            time_check_threshold = now_cet - timedelta(minutes=checkTime)

            return received_time_cet > time_check_threshold
        except Exception as e:
            print(f"Error parsing date: {e}")
            return False
