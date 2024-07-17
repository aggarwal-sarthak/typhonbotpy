import os
from dotenv import load_dotenv

class Env():
    def __init__(self) -> None:
        load_dotenv()
        self._token = os.environ.get("TOKEN")
        self._prefix = os.environ.get("PREFIX")
        self._mongo_uri = os.environ.get("MONGO_URI")
        self._rapid_token = os.environ.get("RAPID_TOKEN")
        self._owner_ids = os.environ.get("OWNER_IDS")
        self._color = os.environ.get("COLOR")
        self._join_logs = os.environ.get("JOIN_LOGS")
        self._leave_logs = os.environ.get("LEAVE_LOGS")
        self._error_logs = os.environ.get("ERROR_LOGS")
        self._update_logs = os.environ.get("UPDATE_LOGS")
        self._bot_logs = os.environ.get("BOT_LOGS")

    @property
    def token(self):
        return self._token

    @property
    def prefix(self):
        return self._prefix

    @property
    def mongo_uri(self):
        return self._mongo_uri

    @property
    def rapid_token(self):
        return self._rapid_token

    @property
    def owner_ids(self):
        return self._owner_ids

    @property
    def color(self):
        return self._color

    @property
    def join_logs(self):
        return self._join_logs

    @property
    def leave_logs(self):
        return self._leave_logs

    @property
    def error_logs(self):
        return self._error_logs

    @property
    def update_logs(self):
        return self._update_logs

    @property
    def bot_logs(self):
        return self._bot_logs
