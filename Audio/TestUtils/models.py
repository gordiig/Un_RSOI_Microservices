from rest_framework.test import APIClient
from django.test import TestCase


def api_response_decorator(method_to_decorate):
    def wrapper(self, url: str, data: dict={}, expected_status_code: int=200):
        client = APIClient()

        response = method_to_decorate(self, url=url, data=data, expected_status_code=expected_status_code,
                                      client=client)

        self.assertEqual(response.status_code, expected_status_code,
                         msg=f'Respone\'s status code for url {url} is {response.status_code}, '
                             f'expected {expected_status_code}')
        json_response = {}
        try:
            json_response = response.json()
        except TypeError:
            pass
        finally:
            return json_response
    return wrapper


class BaseTestCase(TestCase):
    def setUp(self):
        self.url_prefix = '/api/'

    @api_response_decorator
    def get_response_and_check_status(self, url: str, data: dict={}, expected_status_code: int=200, client=None):
        response = client.get(url)
        return response

    @api_response_decorator
    def post_response_and_check_status(self, url: str, data: dict = {}, expected_status_code: int = 201, client=None):
        response = client.post(url, data=data)
        return response

    @api_response_decorator
    def patch_response_and_check_status(self, url: str, data: dict = {}, expected_status_code: int = 200, client=None):
        response = client.patch(url, data=data)
        return response

    @api_response_decorator
    def delete_response_and_check_status(self, url: str, data: dict = {}, expected_status_code: int = 204, client=None):
        response = client.delete(url)
        return response

    @api_response_decorator
    def put_response_and_check_status(self, url: str, data: dict = {}, expected_status_code: int = 200, client=None):
        response = client.put(url, data=data)
        return response
