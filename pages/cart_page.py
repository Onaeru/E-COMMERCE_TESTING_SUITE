from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    # Locators for the cart page
    CART_TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "[id*='remove']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/cart.html"

    def is_cart_page_loaded(self):
        # Check if the cart page is loaded
        return self.is_element_present(self.CART_TITLE) and "Your Cart" in self.find_element(self.CART_TITLE).text
    
    def get_cart_items_count(self):
        # Get the number of items in the cart
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def proceed_to_checkout(self):
        # Proceed to checkout
        checkout_button = self.find_clickeable_element(self.CHECKOUT_BUTTON)
        checkout_button.click()
        return self
    
    def continue_shopping(self):
        # Continue shopping
        continue_shopping_button = self.find_clickeable_element(self.CONTINUE_SHOPPING_BUTTON)
        continue_shopping_button.click()
        return self
    
    def remove_item(self, item_index=0):
        # Remove an item from the cart
        remove_buttons = self.find_clickeable_element(self.REMOVE_BUTTONS[item_index])
        if remove_buttons and item_index < len(self.REMOVE_BUTTONS):
            remove_buttons[item_index].click()
        return self