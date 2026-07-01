import re
import json
import uuid
from datetime import datetime


class Utils:

    @staticmethod
    def validate_email(email):
        """
        Validate email format.
        """
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def clean_text(text):
        """
        Remove extra spaces and newlines.
        """
        return " ".join(text.strip().split())

    @staticmethod
    def current_timestamp():
        """
        Return current timestamp.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_ticket_id():
        """
        Generate unique ticket ID.
        """
        return str(uuid.uuid4())[:8].upper()

    @staticmethod
    def save_json(filename, data):
        """
        Save dictionary/list to JSON file.
        """
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_json(filename):
        """
        Load JSON file.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def write_log(message, logfile="logs.txt"):
        """
        Write log message.
        """
        with open(logfile, "a", encoding="utf-8") as file:
            file.write(
                f"[{Utils.current_timestamp()}] {message}\n"
            )

    @staticmethod
    def format_response(answer, source="AI Assistant"):
        """
        Format chatbot response.
        """
        return {
            "response": answer,
            "source": source,
            "timestamp": Utils.current_timestamp()
        }

    @staticmethod
    def truncate_text(text, max_length=200):
        """
        Shorten long text.
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def validate_priority(priority):
        """
        Validate ticket priority.
        """
        valid = ["Low", "Medium", "High", "Critical"]
        return priority in valid
