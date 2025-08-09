from api.base_api import BaseAPI

class ProductsAPI(BaseAPI):

    def __init__(self):
        super().__init__()
        self.endpoint_base = "/products"

    # Get all products
    def get_all_products(self):
        return self.get(self.endpoint_base)
    
    # Update product stock
    def update_product_stock(self, product_id, new_stock):
        return self.put(f"{self.endpoint_base}/{product_id}/stock", 
                        data={"stock": new_stock})
    
    # Get specific product, using 
    def get_product_by_id(self, product_id):
        response = self.get_all_products()
        if response.status_code == 200:
            products = response.json()['products']
            for product in products:
                if product['id'] == product_id:
                    return product
        return None