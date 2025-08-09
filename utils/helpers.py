import time
import random
from faker import Faker

fake = Faker()

class TestHelpers:
    @staticmethod
    def generate_test_user():
        # Generate a random test user
        return {
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),     
            "last_name": fake.last_name(),
            "password": fake.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            )
        }
    
    @staticmethod
    def wait_random(min_seconds=1, max_seconds=3):
        # Wait for a random amount of time to simulate human interaction
        time.sleep(random.uniform(min_seconds, max_seconds))

    @staticmethod
    def take_screenshot(driver, test_name):

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = f"{test_name}_{timestamp}.png"
        driver.save_screenshot(f"screenshots/{screenshot_name}")
        return screenshot_name