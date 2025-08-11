import pytest
from api.endpoints.users_api import UsersAPI
from api.endpoints.products_api import ProductsAPI
from api.endpoints.orders_api import OrdersAPI
from utils.db_utils import DatabaseUtils
from utils.helpers import TestHelpers

class TestDatabaseValidations:

    # Setup for each test 
    @pytest.fixture(autouse=True)
    def setup(self):
        self.db = DatabaseUtils()
        self.users_api = UsersAPI()
        self.products_api = ProductsAPI()
        self.orders_api = OrdersAPI()

    # Cleanup after each test
    @pytest.fixture(scope="function")
    def cleanup_after_test(self):
        yield
        self.db.reset_product_stocks()

    # Verify that the user is created in the database
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_user_creation_in_database(self):

        user_data = TestHelpers.generate_test_user()
        initial_user_count = self.db.get_user_count()

        response = self.users_api.create_user(user_data)

        assert response.status_code == 201

        final_user_count = self.db.get_user_count()
        assert final_user_count == initial_user_count + 1, \
            f"User was not created in the database. Expected: {initial_user_count + 1}. Actual: {final_user_count}"
        
        db_user = self.db.get_user_by_username(user_data['username'])
        assert db_user is not None, "User was not created in the database."
        assert db_user[1] == user_data['username']
        assert db_user[2] == user_data['email']
        assert db_user[3] == user_data['first_name']
        assert db_user[4] == user_data['last_name']

    # Verify that the product stock is updated in the database
    @pytest.mark.integration
    def test_product_stock_update_in_database(self, cleanup_after_test):

        product_id = 1
        new_stock = 50
        initial_stock = self.db.get_product_stock(product_id)

        response = self.products_api.update_product_stock(product_id, new_stock)

        assert response.status_code == 200

        db_stock = self.db.get_product_stock(product_id)
        assert db_stock == new_stock, \
        f"Product stock was not updated in the database. Expected: {new_stock}. Actual: {db_stock}"

    # Verify that the order is created in the database and the product stock is updated
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_order_creation_and_stock_reduction(self, cleanup_after_test):
        
        response, user_data = self.users_api.create_valid_user()
        user_id = response.json()['id']

        product_id = 2
        quantity = 3
        initial_stock = self.db.get_product_stock(product_id)

        response = self.orders_api.create_simple_order(user_id, product_id, quantity)

        # Verify that the order was created
        assert response.status_code == 201
        order_data = response.json()
        order_id = order_data['order_id']

        db_order = self.db.get_order_details(order_id)
        assert db_order is not None, "Order was not created in the database."
        assert db_order[1] == user_id, "Order was not created for the correct user."
        assert db_order[3] == "completed", "Order was not completed."

        # Verify that the order item was created
        items_count = self.db.get_order_items_count(order_id)
        assert items_count == 1, "Order item was not created in the database."

        # Verify that the product stock was updated
        final_stock = self.db.get_product_stock(product_id)
        expected_stock = initial_stock - quantity
        assert final_stock == expected_stock, \
            f"Product stock was not updated in the database. Expected: {expected_stock}. Actual: {final_stock}"
        
    
    # Verify that multiple orders are created in the database and the product stock is updated
    @pytest.mark.integration
    def test_multiple_orders_stock_tracking(self, cleanup_after_test):
        response1, _ = self.users_api.create_valid_user()
        user_id_1 = response1.json()['id']

        response2, _ = self.users_api.create_valid_user()
        user_id_2 = response2.json()['id']

        product_id = 1
        initial_stock = self.db.get_product_stock(product_id)

        order1_response = self.orders_api.create_simple_order(user_id_1, product_id, 2)
        order2_response = self.orders_api.create_simple_order(user_id_2, product_id, 3)

        assert order1_response.status_code == 201
        assert order2_response.status_code == 201

        final_stock = self.db.get_product_stock(product_id)
        expected_stock = initial_stock - 2 - 3
        assert final_stock == expected_stock, \
            f"Product stock was not updated in the database. Expected: {expected_stock}. Actual: {final_stock}"
        
        orders_user_1 = self.db.get_orders_by_user(user_id_1)
        orders_user_2 = self.db.get_orders_by_user(user_id_2)

        assert len(orders_user_1) >= 1, "User 1 should have more than 1 order"
        assert len(orders_user_2) >= 1, "User 2 should have more than 1 order"

    # Verify that the stock dont update if the order fails
    @pytest.mark.integration
    @pytest.mark.regression
    def test_order_failure_stock_rollback(self, cleanup_after_test):
        response, _ = self.users_api.create_valid_user()
        user_id = response.json()['id']

        product_id = 1

        self.products_api.update_product_stock(product_id, 2)
        stock_before_failed_order = self.db.get_product_stock(product_id)

        response = self.orders_api.create_simple_order(user_id, product_id, 10)

        assert response.status_code == 400

        stock_after_failed_order = self.db.get_product_stock(product_id)
        assert stock_after_failed_order == stock_before_failed_order, \
            f"Product stock was updated in the database. Expected: {stock_before_failed_order}. Actual: {stock_after_failed_order}"