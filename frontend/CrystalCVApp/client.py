from kivy.network.urlrequest import UrlRequest
import json


class Client:
    api_host = "http://127.0.0.1:5000/api/v1"
    app: None

    def __init__(self, app):
        self.app = app

    def register(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        url = f"{self.api_host}/register"
        data = json.dumps(data)
        headers = {
            'Content-type': 'application/json',
        }
        resp = UrlRequest(
            url,
            req_body=data,
            req_headers=headers,
            on_success=self.app.register_success,
            on_error=self.app.error,
            on_failure=self.app.error,
        )

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        url = f"{self.api_host}/login"
        data = json.dumps(data)
        resp = UrlRequest(
            url,
            req_body=data,
            on_success=self.app.login_success,
            on_error=self.app.error,
            on_failure=self.app.error,
        )