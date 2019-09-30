import requests
import json
import re
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
            response = requests.post(url=url, json=data, headers=headers)
        except requests.exceptions.BaseHTTPError:
            return None
        return response

    @staticmethod
    def __find_limit_and_offset_in_link(link: str) -> (int, int):
        limit_substr = re.findall(r'limit=\d+', link)
        offset_substr = re.findall(r'offset=\d+', link)
        limit = re.findall(r'\d+', limit_substr[0])
        offset = [0]
        if len(offset_substr) != 0:
            offset = re.findall(r'\d+', offset_substr[0])
        return limit[0], offset[0]

    @staticmethod
    def __next_and_prev_links_to_params__(data: dict) -> dict:
        try:
            next_link, prev_link = data['next'], data['previous']
        except (KeyError, TypeError):
            return data
        if next_link:
            limit, offset = Requester.__find_limit_and_offset_in_link(next_link)
            data['next'] = f'?limit={limit}&offset={offset}'
        if prev_link:
            limit, offset = Requester.__find_limit_and_offset_in_link(prev_link)
            data['previous'] = f'?limit={limit}&offset={offset}'
        return data

    # MARK: - Auth
    @staticmethod
    def authenticate(data: dict) -> Union[str, Tuple[Dict, int]]:
        response = Requester.perform_post_request(Requester.AUTH_HOST + 'token-auth/', data=data)
        return response.json(), response.status_code

    @staticmethod
    def register(data: dict) -> Tuple[Dict, int]:
        response = Requester.perform_post_request(url=Requester.AUTH_HOST + 'register/', data=data)
        return response.json(), response.status_code

    @staticmethod
    def get_user_info(token: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(url=Requester.AUTH_HOST + 'user_info/', headers={
            'Authorization': f'Token {token}',
        })
        return response.json(), response.status_code

    # MARK: - Images
    @staticmethod
    def get_images(limit_and_offset: (int, int) = None) -> Tuple[Union[List, dict], int]:
        host = Requester.IMAGES_HOST
        if limit_and_offset is not None:
            host += f'?limit={limit_and_offset[0]}&offset={limit_and_offset[1]}'
        response = Requester.perform_get_request(host)
        if response is None:
            return Requester.ERROR_RETURN
        response_json = Requester.__next_and_prev_links_to_params__(response.json())
        return response_json, response.status_code

    @staticmethod
    def get_concrete_image(uuid: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(Requester.IMAGES_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    # MARK: - Audio
    @staticmethod
    def get_audios(limit_and_offset: (int, int) = None) -> Tuple[Union[List, dict], int]:
        host = Requester.AUDIOS_HOST
        if limit_and_offset is not None:
            host += f'?limit={limit_and_offset[0]}&offset={limit_and_offset[1]}'
        response = Requester.perform_get_request(host)
        if response is None:
            return Requester.ERROR_RETURN
        response_json = Requester.__next_and_prev_links_to_params__(response.json())
        return response_json, response.status_code

    @staticmethod
    def get_concrete_audio(uuid: str) -> Tuple[Dict, int]:
        response = Requester.perform_get_request(Requester.AUDIOS_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        try:
            return response.json(), response.status_code
        except json.JSONDecodeError:
            return response.text, response.status_code

    # MARK: - Messages
    @staticmethod
    def __get_and_set_message_image(message: Dict) -> Dict:
        image_uuid = message['image_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if image_uuid is not None:
            image_json, image_status = Requester.get_concrete_image(image_uuid)
            if image_status != 200:
                if (not isinstance(image_json, dict)) and len(image_json) == 0:
                    raise ImageGetError(code=image_status,
                                        err_json={'error': f'Error with getting image, uuid: {image_uuid}!'})
                raise ImageGetError(code=image_status, err_json=image_json)
            message['image'] = image_json
        return message

    @staticmethod
    def __get_and_set_message_audio(message: Dict) -> Dict:
        audio_uuid = message['audio_uuid']  # Можеть быть кей еррор, поймаем в гет_мессаджес
        if audio_uuid is not None:
            audio_json, audio_status = Requester.get_concrete_audio(audio_uuid)
            if audio_status != 200:
                if (not isinstance(audio_json, dict)) and len(audio_json) == 0:
                    raise AudioGetError(code=audio_status,
                                        err_json={'error': f'Error with getting audio, uuid: {audio_uuid}'})
                raise AudioGetError(code=audio_status, err_json=audio_json)
            message['audio'] = audio_json
        return message

    @staticmethod
    def __get_and_set_message_attachments(message: Dict) -> Dict:
        message = Requester.__get_and_set_message_audio(message)
        message = Requester.__get_and_set_message_image(message)
        return message

    @staticmethod
    def get_messages(user_id: int, limit_and_offset: (int, int) = None) -> Tuple[Union[List, Dict], int]:
        # Получаем сообщения
        host = Requester.MESSAGES_HOST + f'?user_id={user_id}'
        if limit_and_offset is not None:
            host += f'&limit={limit_and_offset[0]}&offset={limit_and_offset[1]}'
        response = Requester.perform_get_request(host)
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = Requester.__next_and_prev_links_to_params__(response.json())
        return response_json, 200

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
