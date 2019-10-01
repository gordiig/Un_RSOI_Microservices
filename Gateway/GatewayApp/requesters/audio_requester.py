from typing import Tuple
from GatewayApp.requesters.requester import Requester


class AudioRequester(Requester):
    HOST = Requester.BASE_HOST + ':8004/api/audio/'

    def get_audios(self, request) -> Tuple[dict, int]:
        host = self.HOST
        l_o = self.get_limit_offset_from_request(request)
        if l_o is not None:
            host += f'?limit={l_o[0]}&offset={l_o[1]}'
        response = self.perform_get_request(host)
        if response is None:
            return self.ERROR_RETURN
        response_json = self.next_and_prev_links_to_params(self.get_valid_json_from_response(response))
        return response_json, response.status_code

    def get_concrete_audio(self, request, uuid: str) -> Tuple[dict, int]:
        response = self.perform_get_request(self.HOST + uuid + '/')
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def post_audio(self, request, data: dict) -> Tuple[dict, int]:
        response = self.perform_post_request(self.HOST, data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def patch_audio(self, request, uuid: str, data: dict) -> Tuple[dict, int]:
        response = self.perform_patch_request(self.HOST + uuid + '/', data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def delete_audio(self, request, uuid: str) -> Tuple[dict, int]:
        response = self.perform_delete_request(self.HOST + uuid + '/')
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code
