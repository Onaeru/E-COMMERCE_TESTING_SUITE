import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://www.saucedemo.com/api")
    BROWSER = os.getenv("BROWSER", "chrome")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 20))

    # User credentials
    VALID_USER = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    LOCKED_USER = "locked_out_user"
    PROBLEM_USER = "problem_user"

    @classmethod
    def get_user_credentials(cls, user_type = "standard"):
        users = {
            "standard": (cls.VALID_USER, cls.VALID_PASSWORD),
            "locked": (cls.LOCKED_USER, cls.VALID_PASSWORD),
            "problem": (cls.PROBLEM_USER, cls.VALID_PASSWORD)
        }
        return users.get(user_type, users["standard"])
