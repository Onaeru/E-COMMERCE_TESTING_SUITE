import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import TestHelpers

class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup_with_cart_items(self, driver):
        # Setup for each test
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.products_page = ProductsPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)

        # Login with a valid user and add a product to the cart and proceed to checkout
        self.login_page.open()
        self.login_page.login_with_valid_user()
        self.products_page.add_product_to_cart("backpack")
        self.products_page.add_product_to_cart("bike light")
        self.products_page.go_to_cart()
        self.cart_page.proceed_to_checkout()

    @pytest.mark.smoke
    def test_successfull_checkout_flow(self):
        # Fill in the checkout information
        test_user = TestHelpers.generate_test_user()

        self.checkout_page.fill_checkout_information(
            test_user["first_name"],
            test_user["last_name"],
            "12345"
        )
        print(f"First name: {test_user['first_name']}")
        print(f"Last name: {test_user['last_name']}")
        print(f"Postal code: 12345")

        self.checkout_page.continue_checkout()

        # Check if the checkout overview page is loaded
        assert self.checkout_page.is_checkout_overview_loaded(), \
            "Checkout overview page is not loaded after filling in the checkout information and continuing to checkout."
        
        # Check if the item total, tax amount and total amount are correct
        item_total = self.checkout_page.get_item_total()
        tax_amount = self.checkout_page.get_tax_amount()
        total_amount = self.checkout_page.get_total_amount()

        print(f"Item total: {item_total}")
        print(f"Tax amount: {tax_amount}")
        print(f"Total amount: {total_amount}")

        assert item_total > 0, f"The item total is not correct. Expected: > 0. Actual: {item_total}"
        assert tax_amount > 0, f"The tax amount is not correct. Expected: > 0. Actual: {tax_amount}"
        assert total_amount == item_total + tax_amount, \
            f"The total amount is not correct. Expected: {item_total + tax_amount}. Actual: {total_amount}"
        
        self.checkout_page.finish_checkout()

        # Check if the checkout is complete
        assert self.checkout_page.is_checkout_complete(), \
            "Checkout is not complete after finishing the checkout."
        
        completion_message = self.checkout_page.get_completion_message()
        assert "Your order has been dispatched" in completion_message, \
            f"The completion message is not correct. Expected: 'Your order has been dispatched'. Actual: {completion_message}"
        
        print(f"Completion message: {completion_message}")

    @pytest.mark.regression
    def test_checkout_with_missing_first_name(self):
        # Fill in the checkout information with missing first name
        self.checkout_page.fill_checkout_information("", "Car", "12345")
        self.checkout_page.continue_checkout()

        error_message = self.checkout_page.get_checkout_error_message()
        assert "Error: First Name is required" in error_message, \
            f"The error message is not correct. Expected: 'Error: First Name is required'. Actual: {error_message}"
        
    @pytest.mark.regression
    def test_checkout_with_missing_last_name(self):
        # Fill in the checkout information with missing last name
        self.checkout_page.fill_checkout_information("Lau", "", "12345")
        self.checkout_page.continue_checkout()

        error_message = self.checkout_page.get_checkout_error_message()
        assert "Error: Last Name is required" in error_message, \
            f"The error message is not correct. Expected: 'Error: Last Name is required'. Actual: {error_message}"
        
    @pytest.mark.regression
    def test_checkout_with_missing_postal_code(self):
        # Fill in the checkout information with missing postal code
        self.checkout_page.fill_checkout_information("Lau", "Car", "")
        self.checkout_page.continue_checkout()

        error_message = self.checkout_page.get_checkout_error_message()
        assert "Error: Postal Code is required" in error_message, \
            f"The error message is not correct. Expected: 'Error: Postal Code is required'. Actual: {error_message}"
        
    def test_checkout_cancel_from_information_step(self):
        # Cancel the checkout
        self.checkout_page.cancel_checkout()

        # Check if the cart page is loaded
        assert self.cart_page.is_cart_page_loaded(), \
            "Cart page is not loaded after canceling the checkout."
        
    def test_checkout_back_to_home_after_completion(self):
        # Go back to the home page after completing the checkout
        test_user = TestHelpers.generate_test_user()
        self.checkout_page.fill_checkout_information(
            test_user["first_name"],
            test_user["last_name"],
            "12345"
        )
        self.checkout_page.continue_checkout()
        self.checkout_page.finish_checkout()

        self.checkout_page.back_to_home()

        assert self.products_page.is_products_page_loaded(), \
            "Products page is not loaded after going back to the home page."
        
        # Check if the cart is empty after going back to the home page
        cart_count = self.products_page.get_cart_items_count()
        assert cart_count == 0, \
            f"The number of items in the cart expected is 0. Actual: {cart_count}"