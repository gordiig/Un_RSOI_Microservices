import pybreaker as pb
from typing import Tuple
from GatewayApp.requesters.requester import Requester
from GatewayApp.Queue.Queue import Queue


class ImagesRequester(Requester):
    HOST = Requester.BASE_HOST + ':8003/api/images/'

    db_breaker = pb.CircuitBreaker(fail_max=2, reset_timeout=10)

    # MARK: - Requests for CB
    @db_breaker
    def _perform_get_request(self, host: str):
        response = self.perform_get_request(host)
        if not response:
            raise ValueError
        return response

    def _perform_post_request(self, host: str, data: dict):
        response = self.perform_post_request(host, data=data)
        if not response:
            raise ValueError
        return response

    def _perform_patch_request(self, host: str, data: dict):
        response = self.perform_patch_request(host, data=data)
        if not response:
            raise ValueError
        return response

    def _perform_delete_request(self, host: str):
        response = self.perform_delete_request(host)
        if not response:
            raise ValueError
        return response

    def get_images(self, request) -> Tuple[dict, int]:
        host = self.HOST
        l_o = self.get_limit_offset_from_request(request)
        if l_o is not None:
            host += f'?limit={l_o[0]}&offset={l_o[1]}'
        try:
            response = self._perform_get_request(host)
        except ValueError:
            return self.ERROR_RETURN
        except pb.CircuitBreakerError:
            return self.PB_ERROR_RETURN('Images')
        response_json = self.next_and_prev_links_to_params(self.get_valid_json_from_response(response))
        Queue.fire_image_tasks()
        return response_json, response.status_code

    def get_concrete_image(self, request, uuid: str) -> Tuple[dict, int]:
        try:
            response = self._perform_get_request(self.HOST + f'{uuid}/')
        except ValueError:
            return self.ERROR_RETURN
        except pb.CircuitBreakerError:
            return self.PB_ERROR_RETURN('Images')
        Queue.fire_image_tasks()
        return self.get_valid_json_from_response(response), response.status_code

    def post_image(self, request, data: dict) -> Tuple[dict, int]:
        try:
            response = self._perform_post_request(self.HOST, data=data)
        except ValueError:
            Queue.add_image_task(request, data=data)
            return self.ERROR_RETURN
        except pb.CircuitBreakerError:
            Queue.add_image_task(request, data=data)
            return self.PB_ERROR_RETURN('Images')
        Queue.fire_image_tasks()
        return self.get_valid_json_from_response(response), response.status_code

    def patch_image(self, request, uuid: str, data: dict) -> Tuple[dict, int]:
        try:
            response = self._perform_patch_request(self.HOST + f'{uuid}/', data=data)
        except ValueError:
            Queue.add_image_task(request, uuid=uuid, data=data)
            return self.ERROR_RETURN
        except pb.CircuitBreakerError:
            Queue.add_image_task(request, uuid=uuid, data=data)
            return self.PB_ERROR_RETURN('Images')
        Queue.fire_image_tasks()
        return self.get_valid_json_from_response(response), response.status_code

    def delete_image(self, request, uuid: str) -> Tuple[dict, int]:
        try:
            response = self._perform_delete_request(self.HOST + f'{uuid}/')
        except ValueError:
            Queue.add_image_task(request, uuid=uuid)
            return self.ERROR_RETURN
        except pb.CircuitBreakerError:
            Queue.add_image_task(request, uuid=uuid)
            return self.PB_ERROR_RETURN('Images')
        Queue.fire_image_tasks()
        return self.get_valid_json_from_response(response), response.status_code
