from typing import Union
from GatewayApp.requesters.audio_requester import AudioRequester
from GatewayApp.requesters.images_requester import ImagesRequester


class Queue:
    AUDIO, IMAGE = 'audio', 'image'

    def __init__(self):
        self._queue = []

    def _add_task_to_queue(self, request, data, uuid, ttype):
        self._queue.append({
            'request': request,
            'data': data,
            'uuid': uuid,
            'type': ttype,
        })

    def add_image_task(self, request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        self._add_task_to_queue(request, data, uuid, ttype=Queue.IMAGE)

    def add_audio_task(self, request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        self._add_task_to_queue(request, data, uuid, ttype=Queue.AUDIO)

    def fire_audio_tasks(self):
        atasks = list(filter(lambda x: x['type'] == Queue.AUDIO, self._queue))
        ar = AudioRequester()
        ok_code = 000
        tasks_to_delete = []
        for i, task in atasks:
            if task['request'].method == 'POST':
                _, code = ar.post_audio(task['request'], task['data'])
                ok_code = 201
            elif task['request'].method == 'PATCH':
                _, code = ar.patch_audio(task['request'], task['uuid'], task['data'])
                ok_code = 202
            elif task['request'].method == 'DELETE':
                _, code = ar.delete_audio(task['request'], task['uuid'])
                ok_code = 204
            else:
                code = -1
            if code == ok_code:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            self._queue.remove(task)

    def fire_image_tasks(self):
        itasks = list(filter(lambda x: x['type'] == Queue.IMAGE, self._queue))
        ir = ImagesRequester()
        ok_code = 000
        tasks_to_delete = []
        for task in itasks:
            if task['request'].method == 'POST':
                _, code = ir.post_image(task['request'], task['data'])
                ok_code = 201
            elif task['request'].method == 'PATCH':
                _, code = ir.patch_image(task['request'], task['uuid'], task['data'])
                ok_code = 202
            elif task['request'].method == 'DELETE':
                _, code = ir.delete_image(task['request'], task['uuid'])
                ok_code = 204
            else:
                code = -1
            if code == ok_code:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            self._queue.remove(task)
