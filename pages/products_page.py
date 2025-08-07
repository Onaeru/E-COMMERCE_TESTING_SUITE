from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class ProductsPage(BasePage):

    # Locators
    PRODUCTS_TITTLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    # All items have different ID is that why I used *, 
    # because I don't know how many items are on the page
    # and I don't want to hardcode the ID
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[id*='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "[id*='remove']")
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    PRODUCT_SORT = (By.CSS_SELECTOR, ".product_sort_container")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # Specific items locators for tests
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BIKE_LIGHT_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-bike-light")

    def __init__(self, driver):
        # Initialize the products page
        super().__init__(driver)
        self.url = "/inventory.html"

    def is_products_page_loaded(self):
        # Check if the products page is loaded
        return self.is_element_present(self.PRODUCTS_TITTLE) and "Products" in self.find_element(self.PRODUCTS_TITTLE).text
    
    def get_products_count(self):
        # Get the number of products on the page
        # * is used because find_elements needs two arguments, * is used to unpack the tuple
        products = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(products)
    
    def add_product_to_cart(self, product_name="backpack"):
        # Add a specific product to the cart
        if product_name.lower() == "backpack":
            button = self.find_clickeable_element(self.BACKPACK_ADD_BUTTON)
        elif product_name.lower() == "bike light":
            button = self.find_clickeable_element(self.BIKE_LIGHT_ADD_BUTTON)
        else:
            # Add any other product available
            button = self.find_clickeable_element(self.ADD_TO_CART_BUTTONS)
        
        button.click()
        return self
    
    def get_cart_items_count(self):
        # Get the number of items in the cart
        if self.is_element_present(self.SHOPPING_CART_BADGE):
            badge_text = self.find_element(self.SHOPPING_CART_BADGE).text
            return int(badge_text) if badge_text.isdigit() else 0
        return 0
    
    def go_to_cart(self):
        # Go to the cart
        cart_link = self.find_clickeable_element(self.SHOPPING_CART_LINK)
        cart_link.click()

        return self
    
    def logout(self):
        # Open the burger menu
        burger_menu = self.find_clickeable_element(self.BURGER_MENU_BUTTON)
        burger_menu.click()

        # Click on the logout link
        logout_link = self.find_clickeable_element(self.LOGOUT_LINK)
        logout_link.click()
        return self
    
    def sort_products(self, sort_option="za"):
        # Sort the products
        sort_dropdown = self.find_clickeable_element(self.PRODUCT_SORT)
        sort_dropdown.click()
    
        select = Select(sort_dropdown)
        select.select_by_value(sort_option)
        return self
