from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):

    # Step 1 - Your Information
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step 2 - Overview
    CHECKOUT_SUMMARY_CONTAINER = (By.ID, "checkout_summary_container")
    ITEM_TOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    # Step 3 - Complete
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    PONY_EXPRESS_IMAGE = (By.CSS_SELECTOR, ".pony_express")

    def __init__(self, driver):
        super().__init__(driver)
    
    # Step 1
    def fill_checkout_information(self, first_name, last_name, postal_code):
        # Fill in the checkout information
        self.find_element(self.FIRST_NAME_FIELD).send_keys(first_name)
        self.find_element(self.LAST_NAME_FIELD).send_keys(last_name)
        self.find_element(self.POSTAL_CODE_FIELD).send_keys(postal_code)
        return self
    
    def continue_checkout(self):
        # Click the continue button
        self.find_element(self.CONTINUE_BUTTON).click()
        return self
    
    def cancel_checkout(self):
        # Click the cancel button
        self.find_element(self.CANCEL_BUTTON).click()
        return self
    
    def get_checkout_error_message(self):
        # Get the error message
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.find_element(self.ERROR_MESSAGE).text
        return None
    
    # Step 2
    def is_checkout_overview_loaded(self):
        # Check if the checkout overview page is loaded
        return self.is_element_present(self.CHECKOUT_SUMMARY_CONTAINER)
    
    def get_item_total(self):
        # Obtain the item total
        total_text = self.find_element(self.ITEM_TOTAL).text
        # Extract the item total amount "$xx.xx"
        return float(total_text.split("$")[1])
    
    def get_tax_amount(self):
        # Obtain the tax
        tax_text = self.find_element(self.TAX_LABEL).text
        # Extract the tax amount "$xx.xx"
        return float(tax_text.split("$")[1])
    
    def get_total_amount(self):
        # Obtain the total
        total_text = self.find_element(self.TOTAL_LABEL).text
        # Extract the total amount "$xx.xx"
        return float(total_text.split("$")[1])

    def finish_checkout(self):
        # Click the finish button
        self.find_clickeable_element(self.FINISH_BUTTON).click()
        return self
    
    # Step 3
    def is_checkout_complete(self):
        # Check if the checkout is complete
        return (self.is_element_present(self.COMPLETE_HEADER) and
                "Thank you for your order!" in self.find_element(self.COMPLETE_HEADER).text)
    
    def get_completion_message(self):
        # Get the completion message
        if self.is_element_present(self.COMPLETE_TEXT):
            return self.find_element(self.COMPLETE_TEXT).text
        return None
    
    def back_to_home(self):
        # Click the back to home button
        self.find_clickeable_element(self.BACK_HOME_BUTTON).click()
        return self