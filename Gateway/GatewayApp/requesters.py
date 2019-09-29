import requests
import json
from typing import Tuple, Dict, List, Union, Any


class ImageGetError(Exception):
    def __init__(self, code: int, err_json: Dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class AudioGetError(Exception):
    def __init__(self, code: int, err_json: Dict):
        super().__init__()
        self.code = code
        self.err_msg = err_json


class Requester:
    AUTH_HOST = 'http://127.0.0.1:8001/api/'
    MESSAGES_HOST = 'http://127.0.0.1:8002/api/messages/'
    IMAGES_HOST = 'http://127.0.0.1:8003/api/images/'
    AUDIOS_HOST = 'http://127.0.0.1:8004/api/audio/'
    ERROR_RETURN = (json.dumps({'error': 'BaseHTTPError was raised!'}), 500)

    @staticmethod
    def __create_error_message(msg: str) -> Dict:
        return json.dumps({'error': msg})

    @staticmethod
    def perform_get_request(url: str, headers: dict={}) -> Union[requests.Response, None]:
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.BaseHTTPError:
            return None
        return response

    @staticmethod
    def perform_post_request(url: str, data: dict={}, headers: dict={}) -> Union[requests.Response, None]:
        try:
            response = requests.post(url=url, json=json.dumps(data), headers=headers)
        except requests.exceptions.BaseHTTPError:
            return None
        return response

    # MARK: - Auth
    @staticmethod
    def authenticate(username: str, password: str) -> Union[str, Tuple[Dict, int]]:
        response = Requester.perform_post_request(Requester.AUTH_HOST + 'token-auth/', data={
            'username': username,
            'password': password,
        })
        return response.json(), response.status_code

    @staticmethod
    def register(username: str, email: str, password: str) -> Tuple[Dict, int]:
        response = Requester.perform_post_request(url=Requester.AUTH_HOST + 'register/', data={
            'username': username,
            'password': password,
            'email': email,
        })
        return response.json(), response.status_code

    @staticmethod
    def get_user_info(token: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(url=Requester.AUTH_HOST + 'user_info/', headers={
            'Authorization': f'Token {token}',
        })
        return response.json(), response.status_code

    # MARK: - Images
    @staticmethod
    def get_images() -> Tuple[List, int]:
        response = Requester.perform_get_request(Requester.IMAGES_HOST)
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    @staticmethod
    def get_concrete_image(uuid: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(Requester.IMAGES_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    # MARK: - Audio
    @staticmethod
    def get_audios() -> Tuple[List, int]:
        response = Requester.perform_get_request(Requester.AUDIOS_HOST)
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    @staticmethod
    def get_concrete_audio(uuid: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(Requester.AUDIOS_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    # MARK: - Messages
    @staticmethod
    def __get_and_set_message_image(message: Dict) -> Dict:
        image_uuid = message['image_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if image_uuid is not None:
            image_json, image_status = Requester.get_concrete_image(image_uuid)
            if image_status != 200:
                raise ImageGetError(code=image_status, err_json=image_json)
            message['image'] = image_json
        return message

    @staticmethod
    def __get_and_set_message_audio(message: Dict) -> Dict:
        audio_uuid = message['audio_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if audio_uuid is not None:
            audio_json, audio_status = Requester.get_concrete_audio(audio_uuid)
            if audio_status != 200:
                raise AudioGetError(code=audio_status, err_json=audio_json)
            message['audio'] = audio_json
        return message

    @staticmethod
    def __get_and_set_message_attachments(message: Dict) -> Dict:
        message = Requester.__get_and_set_message_audio(message)
        message = Requester.__get_and_set_message_audio(message)
        return message

    @staticmethod
    def get_messages() -> Tuple[Union[List, Dict], int]:
        # Получаем сообщения
        response = Requester.perform_get_request(Requester.MESSAGES_HOST)
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = response.json()
        ans = []
        # Прикрепляем картинку и аудио
        for msg in response_json:
            try:
                ans.append(Requester.__get_and_set_message_attachments(msg))
            except KeyError:
                return (Requester.__create_error_message('Key error was raised, no image or audio uuid in message json!'),
                        500)
            except (ImageGetError, AudioGetError) as e:
                return e.err_msg, e.code
        return ans, 200

    @staticmethod
    def get_concrete_message(uuid: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(Requester.MESSAGES_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = response.json()
        try:
            ans = Requester.__get_and_set_message_attachments(response_json)
        except KeyError:
            return (Requester.__create_error_message('Key error was raised, no image or audio uuid in message json!'),
                    500)
        except (ImageGetError, AudioGetError) as e:
            return e.err_msg, e.code
        return ans, 200
