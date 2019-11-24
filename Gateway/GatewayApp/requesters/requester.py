import requests
import json
import re
from typing import Tuple, Dict, List, Union, Any


class Requester:
    BASE_HOST = 'http://127.0.0.1'
    AUTH_HOST = 'http://127.0.0.1:8001/api/'
    MESSAGES_HOST = 'http://127.0.0.1:8002/api/messages/'
    ERROR_RETURN = (json.dumps({'error': 'BaseHTTPError was raised!'}), 500)
    def PB_ERROR_RETURN(self, app_name: str):
        return json.dumps({'error': f'Circuit breaker for app {app_name} is on'}), 500


    @staticmethod
    def __create_error_message(msg: str) -> Dict:
        return json.dumps({'error': msg})

    # MARK: - Requests
    def perform_get_request(self, url: str, headers: dict={}) -> Union[requests.Response, None]:
        try:
            response = requests.get(url, headers=headers)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    def perform_post_request(self, url: str, data: dict={}, headers: dict={}) -> Union[requests.Response, None]:
        try:
            response = requests.post(url=url, json=data, headers=headers)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    def perform_delete_request(self, url: str, headers: dict={}) -> Union[requests.Response, None]:
        try:
            response = requests.delete(url=url, headers=headers)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    def perform_patch_request(self, url: str, data: dict={}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            response = requests.patch(url=url, json=data, headers=headers)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    # MARK: - Utility
    def get_limit_offset_from_request(self, request) -> Union[Tuple[int, int], None]:
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
        except KeyError:
            return None
        return limit, offset

    def find_limit_and_offset_in_link(self, link: str) -> (int, int):
        limit_substr = re.findall(r'limit=\d+', link)
        offset_substr = re.findall(r'offset=\d+', link)
        limit = re.findall(r'\d+', limit_substr[0])
        offset = [0]
        if len(offset_substr) != 0:
            offset = re.findall(r'\d+', offset_substr[0])
        return limit[0], offset[0]

    def next_and_prev_links_to_params(self, data: dict) -> dict:
        try:
            next_link, prev_link = data['next'], data['previous']
        except (KeyError, TypeError):
            return data
        if next_link:
            limit, offset = self.find_limit_and_offset_in_link(next_link)
            data['next'] = f'?limit={limit}&offset={offset}'
        if prev_link:
            limit, offset = self.find_limit_and_offset_in_link(prev_link)
            data['previous'] = f'?limit={limit}&offset={offset}'
        return data

    def get_valid_json_from_response(self, response: requests.Response):
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            return response.text

    def get_token_from_request(self, request) -> Union[str, None]:
        token_str = request.META.get('HTTP_AUTHORIZATION')
        try:
            token = token_str[6:]
        except TypeError:
            return None
        return token
