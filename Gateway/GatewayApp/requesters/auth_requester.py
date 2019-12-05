from typing import Tuple
from GatewayApp.requesters.requester import Requester


class AuthRequester(Requester):
    HOST = Requester.BASE_HOST + ':8001/api/'

    def _create_auth_header(self, token: str):
        token_type = 'Bearer' if len(token) < 40 else 'Token'
        return {'Authorization': f'{token_type} {token}'}

    def get_users(self, request) -> Tuple[dict, int]:
        host = self.HOST + 'users/'
        l_o = self.get_limit_offset_from_request(request)
        if l_o:
            host += f'?limit={l_o[0]}&offset={l_o[1]}'
        token = self.get_token_from_request(request)
        response = self.perform_get_request(host, headers=self._create_auth_header(token))
        if response is None:
            return self.ERROR_RETURN
        response_json = self.next_and_prev_links_to_params(self.get_valid_json_from_response(response))
        return response_json, response.status_code

    def get_concrete_user(self, request, user_id: str) -> Tuple[dict, int]:
        token = self.get_token_from_request(request)
        response = self.perform_get_request(self.HOST + f'users/{user_id}/', headers=self._create_auth_header(token))
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def get_user_info(self, request) -> Tuple[dict, int]:
        token = self.get_token_from_request(request)
        if token is None:
            return {}, 403
        response = self.perform_get_request(self.HOST + 'user_info/', headers=self._create_auth_header(token))
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def _delete_users_messages(self, request) -> Tuple[dict, int]:
        from GatewayApp.requesters.messages_requester import MessagesRequester
        mrequester = MessagesRequester()
        user_json, code = self.get_user_info(request)
        if code != 200:
            return user_json, code
        messages_json, code = mrequester.get_messages(request)
        if code != 200:
            return messages_json, code
        for message in messages_json:
            mrequester.delete_message(request, message['uuid'])
        return {}, 204

    def delete_user(self, request) -> Tuple[dict, int]:
        djson, code = self._delete_users_messages(request)
        if code != 204:
            return djson, code
        token = self.get_token_from_request(request)
        response = self.perform_delete_request(self.HOST + 'user_info/', headers=self._create_auth_header(token))
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def register(self, request, data: dict) -> Tuple[dict, int]:
        response = self.perform_post_request(url=self.HOST + 'register/', data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def authenticate(self, data: dict) -> Tuple[dict, int]:
        response = self.perform_post_request(url=self.HOST + 'token-auth/', data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code
