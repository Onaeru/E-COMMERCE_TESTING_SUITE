import pytest
from api.endpoints.products_api import ProductsAPI

class TestProductsAPI:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.products_api = ProductsAPI()

    # Get all products
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_products(self):

        response = self.products_api.get_all_products()

        self.products_api.validate_status_code(response, 200)
        json_data = self.products_api.validate_json_schema(response, ['products'])

        products = json_data['products']
        assert len(products) >= 6, f"Expected at least 6 products, but found {len(products)}"

        first_product = products[0]
        required_fields = ['id', 'name', 'price', 'stock', 'description']
        for field in required_fields:
            assert field in first_product, f"JSON schema is not correct. Missing field: {field}"
        
        assert first_product['price'] > 0, "Product price should be greater than 0"
        assert first_product['stock'] >= 0, "Product stock should be greater than or equal to 0"


    # Update product stock
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_product_stock_success(self):
        product_id = 1
        new_stock = 25

        initial_product = self.products_api.get_product_by_id(product_id)
        initial_stock = initial_product['stock'] if initial_product else 0

        response = self.products_api.update_product_stock(product_id, new_stock)

        self.products_api.validate_status_code(response, 200)
        json_data = self.products_api.validate_json_schema(response,
            ['message', 'new_stock'])
        
        assert json_data['new_stock'] == new_stock
        assert 'successfully' in json_data['message']

        updated_product = self.products_api.get_product_by_id(product_id)
        assert updated_product['stock'] == new_stock, \
            f"Product stock should be updated to {new_stock}, but is {updated_product['stock']}"
    
    # Update invalid product stock
    @pytest.mark.api
    def test_update_product_stock_invalid_product(self):
        response = self.products_api.update_product_stock(99999, 10)

        self.products_api.validate_status_code(response, 404)
        json_data = response.json()
        assert 'error' in json_data
        assert 'not found' in json_data['error']


    # Get specific products
    @pytest.mark.api
    @pytest.mark.parametrize("product_id,expected_name", [
        (1, "Sauce Labs Backpack"),
        (2, "Sauce Labs Bike Light"),
        (3, "Sauce Labs Bolt T-Shirt")
    ])
    def test_verify_specific_products(self, product_id, expected_name):
        product = self.products_api.get_product_by_id(product_id)

        assert product is not None, f"Product with id {product_id} not found"
        assert product['name'] == expected_name, \
            f"Expected product name to be {expected_name}, but got {product['name']}"
        assert product['id'] == product_id