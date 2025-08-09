import requests
import json

from trio_websocket import Endpoint
from utils.config import Config

class BaseAPI:
    # Initialize the base API
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    # Make a GET request
    def get(self, endpoint, params=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, **kwargs)
        self._log_request_response("GET", url, response, params=params)
        return response
    
    # Make a POST request
    def post(self, endpoint, data=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        json_data = json.dumps(data) if data else None
        response = self.session.post(url, data=json_data, **kwargs)
        self._log_request_response("POST", url, response, data=data)
        return response
    
    # Make a PUT request
    def put(self, endpoint, data=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        json_data = json.dumps(data) if data else None
        response = self.session.put(url, data=json_data, **kwargs)
        self._log_request_response("PUT", url, response, data=data)
        return response
    
    # Make a DELETE request
    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, **kwargs)
        self._log_request_response("DELETE", url, response)
        return response
    
    # Log request and response details
    def _log_request_response(self, method, url, response, data=None, params=None):
        print(f"\n{'='*50}")
        print(f"{method} {url}")
        if params:
            print(f"Params: {params}")
        if data:
            print(f"Data: {data}")
        print(f"Status code: {response.status_code}")
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=4)}")
        except:
            print(f"Response: {response.text}")
        print(f"{'='*50}\n")

    # Validate the status code
    def validate_status_code(self, response, expected_status):
        assert response.status_code == expected_status, \
            f"Status code is not correct. Expected: {expected_status}. Actual: {response.status_code}"

    # Validate the JSON schema        
    def validate_json_schema(self, response, required_fields):
        try:
            json_data = response.json()
            for field in required_fields:
                assert field in json_data, f"JSON schema is not correct. Missing field: {field}"
            return json_data
        except json.JSONDecodeError:
            raise AssertionError(f"JSON schema is not correct. Response: {response.text}")