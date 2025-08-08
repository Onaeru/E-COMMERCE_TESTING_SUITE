from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):

    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CLASS_NAME, "error-button")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/"
    
    def open(self):
        # Open the login page
        return self.open_page(self.url)
    
    def enter_username(self, username):
        # Enter the username
        username_field = self.find_element(self.USERNAME_FIELD)
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    def enter_password(self, password):
        # Enter the password
        password_field = self.find_element(self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login(self):
        # Click on the login button
        login_button = self.find_clickeable_element(self.LOGIN_BUTTON)
        login_button.click()
        return self
    
    def login(self, username, password):
        # Login with the provided credentials
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def login_with_valid_user(self):
        # Login with a valid user
        username, password = Config.get_user_credentials("standard")
        return self.login(username, password)
    
    def get_error_message(self):
        # Get the error message
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.find_element(self.ERROR_MESSAGE).text
        return None
    
    def is_error_displayed(self):
        # Check if the error message is displayed
        return self.is_element_present(self.ERROR_MESSAGE)
        
    def is_login_page_loaded(self):
        # Check if the login page is loaded looking for the login logo
        return self.is_element_present(self.LOGIN_LOGO)
    
    def clear_error(self):
        # Clear the error
        if self.is_element_present(self.ERROR_BUTTON):
            self.find_clickeable_element(self.ERROR_BUTTON).click()
        return self