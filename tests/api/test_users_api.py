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