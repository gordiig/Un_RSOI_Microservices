from typing import Tuple, Union
from GatewayApp.requesters.requester import Requester


class ImageGetError(Exception):
    def __init__(self, code: int, err_json: dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class AudioGetError(Exception):
    def __init__(self, code: int, err_json: dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class MessagesRequester(Requester):
    HOST = Requester.BASE_HOST + ':8002/api/messages/'

    # MARK: - Privates, getiing image and audio
    def __get_and_set_message_image(self, message: dict) -> dict:
        from GatewayApp.requesters.images_requester import ImagesRequester
        image_uuid = message['image_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if image_uuid is not None:
            image_json, image_status = ImagesRequester().get_concrete_image(request=None, uuid=image_uuid)
            if image_status != 200:
                raise ImageGetError(code=image_status, err_json=image_json)
            message['image'] = image_json
        return message

    def __get_and_set_message_audio(self, message: dict) -> dict:
        from GatewayApp.requesters.audio_requester import AudioRequester
        audio_uuid = message['audio_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if audio_uuid is not None:
            audio_json, audio_status = AudioRequester().get_concrete_audio(request=None, uuid=audio_uuid)
            if audio_status != 200:
                raise AudioGetError(code=audio_status, err_json=audio_json)
            message['audio'] = audio_json
        return message

    def __get_and_set_message_attachments(self, message: dict) -> dict:
        message = self.__get_and_set_message_audio(message)
        message = self.__get_and_set_message_image(message)
        return message

    def get_messages(self, request) -> Tuple[dict, int]:
        host = self.HOST
        # User info
        user_json, code = self._get_user_by_token(request)
        if code != 200:
            return user_json, code
        host += f'?user_id={user_json["id"]}'
        # Limit-offset
        l_o = self.get_limit_offset_from_request(request)
        if l_o is not None:
            host += f'&limit={l_o[0]}&offset={l_o[1]}'
        response = self.perform_get_request(host)
        if response is None:
            return self.ERROR_RETURN
        response_json = self.next_and_prev_links_to_params(self.get_valid_json_from_response(response))
        return response_json, response.status_code

    def get_concrete_message(self, request, uuid: str) -> Tuple[dict, int]:
        response = self.perform_get_request(self.HOST + uuid + '/')
        if response is None:
            return self.ERROR_RETURN
        if response.status_code != 200:
            return self.get_valid_json_from_response(response), response.status_code
        valid_json = self.get_valid_json_from_response(response)
        try:
            ans = self.__get_and_set_message_attachments(valid_json)
        except KeyError:
            return {'error': 'Key error was raised, no image or audio uuid in message json!'}, 500
        except (ImageGetError, AudioGetError) as e:
            return e.err_msg, e.code
        return ans, 200

    def _check_if_image_exists(self, image_uuid) -> bool:
        from GatewayApp.requesters.images_requester import ImagesRequester
        _, code = ImagesRequester().get_concrete_image(request=None, uuid=image_uuid)
        return code == 200

    def _check_if_audio_exists(self, audio_uuid) -> bool:
        from GatewayApp.requesters.audio_requester import AudioRequester
        _, code = AudioRequester().get_concrete_audio(request=None, uuid=audio_uuid)
        return code == 200

    def _check_if_user_exists(self, request, user_id) -> bool:
        from GatewayApp.requesters.auth_requester import AuthRequester
        _, code = AuthRequester().get_concrete_user(request=request, user_id=user_id)
        return code == 200

    def _get_user_by_token(self, request) -> Tuple[dict, int]:
        from GatewayApp.requesters.auth_requester import AuthRequester
        user_json, code = AuthRequester().get_user_info(request)
        return user_json, code

    def _check_if_attachments_exist(self, request, data: dict) -> Tuple[dict, int]:
        # Есть ли такая картинка
        if data['image_uuid']:
            if not self._check_if_image_exists(data['image_uuid']):
                return {'error': f'Image with uuid "{data["image_uuid"]}" does not exist!'}, 404
        # Есть ли такое аудио
        if data['audio_uuid']:
            if not self._check_if_audio_exists(data['audio_uuid']):
                return {'error': f'Audio with uuid "{data["audio_uuid"]}" does not exist!'}, 404
        # Есть ли такие юзеры
        if data['to_user_id']:
            if not self._check_if_user_exists(request, data['to_user_id']):
                return {'error': f'User with id "{data["to_user_id"]}" does not exist!'}, 404
        return {}, 200

    def _add_from_user_id_to_data(self, request, data: dict) -> Tuple[dict, int]:
        # Получение айдишника юзера, который пишет
        user_json, code = self._get_user_by_token(request)
        if code != 200:
            return user_json, code
        data['from_user_id'] = user_json['id']
        return data, 200

    def post_message(self, request, data: dict) -> Tuple[dict, int]:
        check_json, code = self._check_if_attachments_exist(request, data)
        if code != 200:
            return check_json, code
        data, code = self._add_from_user_id_to_data(request, data)
        if code != 200:
            return data, code
        response = self.perform_post_request(self.HOST, data=data)
        if response is None:
            return Requester.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def patch_message(self, request, uuid: str, data: dict) -> Tuple[dict, int]:
        check_json, code = self._check_if_attachments_exist(request, data)
        if code != 200:
            return check_json, 200
        data, code = self._add_from_user_id_to_data(request, data)
        if code != 200:
            return data, code
        response = self.perform_patch_request(self.HOST + f'{uuid}/', data=data)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code

    def _delete_image_from_message(self, request, message_json: dict) -> Tuple[dict, int]:
        from GatewayApp.requesters.images_requester import ImagesRequester
        if message_json['image_uuid']:
            del_json, code = ImagesRequester().delete_image(request, message_json['image_uuid'])
            if code not in (204, 404):
                return del_json, code
        return {}, 204

    def _delete_audio_from_message(self, request, message_json: dict) -> Tuple[dict, int]:
        from GatewayApp.requesters.audio_requester import AudioRequester
        if message_json['audio_uuid']:
            del_json, code = AudioRequester().delete_audio(request, message_json['audio_uuid'])
            if code not in (204, 404):
                return del_json, code
        return {}, 204

    def delete_message(self, request, uuid: str) -> Tuple[dict, int]:
        message_json, code = self.get_concrete_message(request, uuid)
        if code != 200:
            return message_json, code
        del_json, code = self._delete_image_from_message(request, message_json)
        if code != 204:
            return del_json, code
        del_json, code = self._delete_audio_from_message(request, message_json)
        if code != 204:
            return del_json, code
        response = self.perform_delete_request(self.HOST + uuid)
        if response is None:
            return self.ERROR_RETURN
        return self.get_valid_json_from_response(response), response.status_code