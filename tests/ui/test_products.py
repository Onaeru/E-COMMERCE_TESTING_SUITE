import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.config import Config

class TestProducts:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        # Setup for each test
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)

        # Login with a valid user
        self.login_page.open()
        self.login_page.login_with_valid_user()

    @pytest.mark.smoke
    def test_products_page_loaded_after_login(self):
        # Check if the products page is loaded
        assert self.products_page.is_products_page_loaded(), \
            "The products page is not correctly loaded after login"
        
        products_count = self.products_page.get_products_count()
        assert products_count > 0, \
            f"There are no products on the page. Count: {products_count}"
        assert products_count == 6, \
            f"The number of products expected is 6. Actual: {products_count}"
        
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self):
        # Add a single product to the cart
        initial_cart_count = self.products_page.get_cart_items_count()

        self.products_page.add_product_to_cart("backpack")

        final_cart_count = self.products_page.get_cart_items_count()
        assert final_cart_count == initial_cart_count + 1, \
            f"The number of items in the cart expected is {initial_cart_count + 1}. Actual: {final_cart_count}"
        assert final_cart_count == 1, \
            f"The number of items in the cart expected is 1. Actual: {final_cart_count}"
        
    @pytest.mark.smoke
    def test_add_multiple_products_to_cart(self):
        # Add multiple products to the cart
        self.products_page.add_product_to_cart("backpack")
        self.products_page.add_product_to_cart("bike light")

        cart_count = self.products_page.get_cart_items_count()
        assert cart_count == 2, \
            f"The number of items in the cart expected is 2. Actual: {cart_count}"

    @pytest.mark.regression
    def test_cart_navigation(self):
        # Add a product to the cart and navigate to the cart

        self.products_page.add_product_to_cart("backpack")

        self.products_page.go_to_cart()

        assert self.cart_page.is_cart_page_loaded(), \
            "The cart page is not correctly loaded"
        
        cart_items = self.cart_page.get_cart_items_count()
        assert cart_items == 1, \
            f"The number of items in the cart expected is 1. Actual: {cart_items}"
    
    def test_logout_functionality(self):
        # Logout
        self.products_page.logout()

        assert self.login_page.is_login_page_loaded(), \
            "The login page is not correctly loaded after logout"
        assert self.driver.current_url.endswith("/"), \
            "The URL is not correct after logout"
        
    @pytest.mark.parametrize("product_name", ["backpack", "bike light"])
    def test_add_different_products_parametrize(self, product_name):
        # Add different products to the cart using parametrize
        self.products_page.add_product_to_cart(product_name)

        cart_count = self.products_page.get_cart_items_count()
        assert cart_count == 1, \
            f"The number of items in the cart expected is 1. Actual: {cart_count}"