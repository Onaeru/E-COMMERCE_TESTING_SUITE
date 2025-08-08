import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import Config
from utils.helpers import TestHelpers

class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
    
    @pytest.mark.smoke
    def test_successful_login_standard_user(self):
        # Login with a valid user
        # username, password = TestHelpers.generate_test_user()
        username, password = Config.get_user_credentials("standard")

        # Open the login page
        self.login_page.open()
        # Login
        self.login_page.login(username, password)

        # Check if the login was successful
        assert self.products_page.is_products_page_loaded(), \
            "The products page is not loaded after successful login"
        assert "inventory.html" in self.driver.current_url, \
            "The URL is not correct after successful login"