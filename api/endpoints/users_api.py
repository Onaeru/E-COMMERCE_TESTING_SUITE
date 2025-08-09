from api.base_api import BaseAPI
from utils.helpers import TestHelpers

class UsersAPI(BaseAPI):

    def __init__(self):
        super().__init__()
        self.endpoint_base = "/users"

    # Get all users
    def get_all_users(self):
        return self.get(self.endpoint_base)
    
    # Get user by ID
    def get_user_by_id(self, user_id):
        return self.get(f"{self.endpoint_base}/{user_id}")
    
    # Create a new user
    def create_user(self, user_data):
        return self.post(self.endpoint_base, data=user_data)
    
    def create_valid_user(self, username=None, email=None):
        user_data = TestHelpers.generate_test_user()

        if username:
            user_data['username'] = username
        if email:
            user_data['email'] = email

        return self.create_user(user_data), user_data
    