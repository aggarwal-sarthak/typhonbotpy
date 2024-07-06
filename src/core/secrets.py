import os
from dotenv import load_dotenv


class Env():
    def __init__(self) -> None:
        load_dotenv()
        self.token = os.environ.get("TOKEN")

    # @property
    # def token(self):
    #     return self.token