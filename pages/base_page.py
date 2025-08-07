from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import Config

class BasePage:
    def __init__(self, driver):
        # Initialize the base page
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.base_url = Config.BASE_URL

    def open_page(self, url=""):
        # Open a page
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)
        return self
    
    def find_element(self, locator, timeout=None):
        # Wait for an element to be present
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_clickeable_element(self, locator, timeout=None):
        # Wait for an element to be clickable
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def is_element_present(self, locator, timeout=5):
        # Check if an element is present on the page
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
                )
            return True
        except TimeoutException:
            return False
        
    def get_page_title(self):
        # Get the title of the current page
        return self.driver.title
    
    def get_current_url(self):
        # Get the URL of the current page
        return self.driver.current_url