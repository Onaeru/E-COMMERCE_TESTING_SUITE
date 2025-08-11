import pytest
from api.endpoints.users_api import UsersAPI
from api.endpoints.products_api import ProductsAPI
from api.endpoints.orders_api import OrdersAPI

class TestOrderAPI:

    # Setup for each test
    @pytest.fixture(autouse=True)
    def setup(self):
        self.users_api = UsersAPI()
        self.products_api = ProductsAPI()
        self.orders_api = OrdersAPI()

    # Create a test user
    @pytest.fixture
    def test_user(self):
        response, user_data = self.users_api.create_valid_user()
        user_json = response.json()
        return user_json['id'], user_data
    
    # Test create order success
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_order_success(self, test_user):

        user_id, _ = test_user
        
        # Get initial product stock
        initial_product = self.products_api.get_product_by_id(1)
        initial_stock = initial_product['stock']
        print(f"User ID: {user_id}, Initial stock: {initial_stock}")

        order_data = {
            "user_id": user_id,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 1
                },{
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }

        response = self.orders_api.create_order(order_data)

        self.orders_api.validate_status_code(response, 201)
        json_data = self.orders_api.validate_json_schema(response, 
            ['order_id', 'total_amount', 'status', 'message'])
        
        # Validate order details
        assert json_data['status'] == 'completed'
        assert json_data['total_amount'] > 0
        assert 'successfully' in json_data['message']

        # Validate product stock was reduced
        updated_product = self.products_api.get_product_by_id(1)
        expected_stock = initial_stock - 2
        assert updated_product['stock'] == expected_stock, \
            f"Product stock should be {expected_stock}, but is {updated_product['stock']}"
        
        # Store order id for future tests
        return json_data['order_id']
    
    # Test create order with insufficient stock
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_order_insufficient_stock(self, test_user):
        
        user_id, _ = test_user

        self.products_api.update_product_stock(1, 1)

        order_data = {
            "user_id": user_id,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 10
                }
            ]
        }
        

        response = self.orders_api.create_order(order_data)

        self.orders_api.validate_status_code(response, 400)
        json_data = response.json()
        assert 'error' in json_data
        assert 'stock' in json_data['error']

    # Test get order by id
    @pytest.mark.api
    def test_get_order_by_id_success(self, test_user):

        user_id, user_data = test_user
        create_response = self.orders_api.create_simple_order(user_id, product_id=1, quantity=1)
        order_id = create_response.json()['order_id']

        response = self.orders_api.get_order_by_id(order_id)

        self.orders_api.validate_status_code(response, 200)
        json_data = self.orders_api.validate_json_schema(response,
            ['order_id', 'user_id', 'username','total_amount', 'status', 'items'])
        
        # Validate order details
        assert json_data['order_id'] == order_id
        assert json_data['user_id'] == user_id
        assert json_data['username'] == user_data['username']
        assert json_data['total_amount'] == 1

        # Validate item structure
        item = json_data['items'][0]
        assert 'product_id' in item
        assert 'product_name' in item
        assert 'quantity' in item
        assert 'price' in item

    # Test get order not found
    @pytest.mark.api
    def test_get_order_not_found(self):
        
        response = self.orders_api.get_order_by_id("non-existent-order-id")

        self.orders_api.validate_status_code(response, 404)
        json_data = response.json()
        assert 'error' in json_data
        assert 'not found' in json_data['error'] 
    

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_order_invalid_user(self):

        order_data = {
            "user_id": 99999,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 1
                }
            ]
        }
        
        response = self.orders_api.create_order(order_data)

        # Status code should be 4xx or 5xx
        assert response.status_code > 400, "Status code should return 4xx or 5xx for invalid user"