from api.base_api import BaseAPI

class OrdersAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.endpoint_base = "/orders"

    # Create a new order
    def create_order(self, order_data):
        return self.post(self.endpoint_base, data=order_data)
    
    # Get an order by ID
    def get_order_by_id(self, order_id):
        return self.get(f"{self.endpoint_base}/{order_id}")
    
    # Create a simple order with default values
    def create_simple_order(self, user_id, product_id=1, quantity=1):
        order_data = {
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": quantity
                }
            ]
        }
        return self.create_order(order_data)