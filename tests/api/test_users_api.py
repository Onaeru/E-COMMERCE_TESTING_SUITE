import pytest
from api.endpoints.users_api import UsersAPI
from utils.helpers import TestHelpers

class TestUsersAPI:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.users_api = UsersAPI()

    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_users(self):
        response = self.users_api.get_all_users()

        self.users_api.validate_status_code(response, 200)
        json_data = self.users_api.validate_json_schema(response, ["users"])

        assert isinstance(json_data['users'], list), \
            "JSON schema is not correct. 'users' field is not a list"
        
    # Create user
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_user_success(self):

        user_data = TestHelpers.generate_test_user()

        response = self.users_api.create_user(user_data)

        self.users_api.validate_status_code(response, 201)
        json_data = self.users_api.validate_json_schema(response, 
            ["id", "username", "email", "first_name", "last_name", "message"])
        
        assert json_data['username'] == user_data['username']
        assert json_data['email'] == user_data['email']
        assert json_data['message'] == "User created successfully" 

        created_user_id = json_data['id']
        assert created_user_id > 0, "The ID of the created user should be greater than 0."

    # Create duplicate user to verify error
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_duplicate_user(self):

        user_data = TestHelpers.generate_test_user()

        response1 = self.users_api.create_user(user_data)
        self.users_api.validate_status_code(response1, 201)

        response2 = self.users_api.create_user(user_data)
        self.users_api.validate_status_code(response2, 409)
        json_data = response2.json()
        assert 'error' in json_data
        assert 'already exists' in json_data['error']

    # Get user by ID success
    @pytest.mark.api
    def test_get_user_by_id_success(self):
        response, user_data = self.users_api.create_valid_user()
        created_user = response.json()
        user_id = created_user['id']
        
        response = self.users_api.get_user_by_id(user_id)
        
        self.users_api.validate_status_code(response, 200)
        json_data = self.users_api.validate_json_schema(response, 
            ['id', 'username', 'email', 'first_name', 'last_name'])
        
        assert json_data['id'] == user_id
        assert json_data['username'] == user_data['username']
        assert json_data['email'] == user_data['email']

    # Get user by ID not found
    @pytest.mark.api
    def test_get_user_by_id_not_found(self):
        response = self.users_api.get_user_by_id(99999)

        self.users_api.validate_status_code(response, 404)
        json_data = response.json()
        assert 'error' in json_data
        assert 'User not found' in json_data['error']