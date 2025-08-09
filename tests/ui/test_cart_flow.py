import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

class TestCartFlow:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        # Setup for each test
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)

        # Login with a valid user and add a product to the cart
        self.login_page.open()
        self.login_page.login_with_valid_user()
        self.products_page.add_product_to_cart("backpack")
        self.products_page.go_to_cart()
    
    @pytest.mark.smoke
    def test_cart_page_displays_added_products(self):

        assert self.cart_page.is_cart_page_loaded(), \
            "The cart page is not correctly loaded"
        
        items_count = self.cart_page.is_cart_page_loaded()
        assert items_count == 1, \
            f"The number of items in the cart expected is 1. Actual: {items_count}"
    
    @pytest.mark.smoke
    def test_cart_page_displays_added_products(self):
        # 

        assert self.cart_page.is_cart_page_loaded(), \
            "The cart page is not correctly loaded"
        
        items_count = self.cart_page.is_cart_page_loaded()
        assert items_count == 1, \
            f"The number of items in the cart expected is 1. Actual: {items_count}"
        
    @pytest.mark.regression
    def test_remove_item_from_cart(self):
        # Remove an item from the cart
        initial_count = self.cart_page.get_cart_items_count()
        
        self.cart_page.remove_item(0)
        
        final_count = self.cart_page.get_cart_items_count()
        assert final_count == initial_count - 1, \
            f"The number of items in the cart expected is {initial_count - 1}. Actual: {final_count}"
        
    def test_continue_shopping_from_cart(self):
        # Continue shopping from the cart

        self.cart_page.continue_shopping()

        assert self.products_page.is_products_page_loaded(), \
            "The products page is not correctly loaded"