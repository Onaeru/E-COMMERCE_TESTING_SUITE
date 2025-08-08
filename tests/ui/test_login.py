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

    def test_login_page_elements_present(self):
        # Verify that the login page elements are present
        self.login_page.open()
        assert self.login_page.is_login_page_loaded(), \
            "The login page is not loaded"
        assert self.login_page.is_element_present(self.login_page.USERNAME_FIELD), \
            "Username field is not present"
        assert self.login_page.is_element_present(self.login_page.PASSWORD_FIELD), \
            "Password field is not present"
        assert self.login_page.is_element_present(self.login_page.LOGIN_BUTTON), \
            "Login button is not present"
        assert self.login_page.is_element_present(self.login_page.LOGIN_LOGO), \
            "Login logo is not present"
        
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
        
    @pytest.mark.smoke
    def test_login_with_invalid_credentials(self):
        # Login with invalid credentials
        invalid_username = "invalid_username"
        invalid_password = "invalid_password"

        # Open the login page
        self.login_page.open()
        # Login
        self.login_page.login(invalid_username, invalid_password)

        assert self.login_page.is_error_displayed(), \
            "The error message is not displayed after login with invalid credentials"
        
        error_message = self.login_page.get_error_message()
        print(f"Error message: {error_message}")
        assert "Username and password do not match any user in this service" in error_message, \
            f"Error message is not correct. Expected: {error_message}"
        
    @pytest.mark.regression
    def test_login_with_locked_user(self):
        # Login with a locked user
        username, password = Config.get_user_credentials("locked")

        self.login_page.open()
        self.login_page.login(username, password)

        assert self.login_page.is_error_displayed(), \
            "The error message is not displayed after login with a locked user"
        
        error_message = self.login_page.get_error_message()
        print(f"Error message: {error_message}")
        assert "Sorry, this user has been locked out." in error_message, \
            f"Error message is not correct. Expected: {error_message}"
        
    @pytest.mark.regression
    def test_login_empty_credentials(self):
        # Login with empty credentials
        self.login_page.open()
        self.login_page.login("", "")

        assert self.login_page.is_error_displayed(), \
            "The error message is not displayed after login with empty credentials"
        
        error_message = self.login_page.get_error_message()
        print(f"Error message: {error_message}")
        assert "Epic sadface: Username is required" in error_message, \
            f"Error message is not correct. Expected: {error_message}"
        
    @pytest.mark.regression
    def test_login_empty_password(self):
        # Login with empty password
        username = "standard_user"
        self.login_page.open()
        self.login_page.login(username, "")

        assert self.login_page.is_error_displayed(), \
            "The error message is not displayed after login with empty password"
        
        error_message = self.login_page.get_error_message()
        print(f"Error message: {error_message}")
        assert "Epic sadface: Password is required" in error_message, \
            f"Error message is not correct. Expected: {error_message}"