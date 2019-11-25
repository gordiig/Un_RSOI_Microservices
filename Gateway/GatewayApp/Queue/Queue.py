from typing import Union
from GatewayApp.requesters.audio_requester import AudioRequester
from GatewayApp.requesters.images_requester import ImagesRequester


class Queue:
    AUDIO, IMAGE = 'audio', 'image'
    queue = []

    @staticmethod
    def _add_task_to_queue(request, data, uuid, ttype):
        Queue.queue.append({
            'request': request,
            'data': data,
            'uuid': uuid,
            'type': ttype,
        })

    @staticmethod
    def add_image_task(request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.IMAGE)

    @staticmethod
    def add_audio_task(request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.AUDIO)

    @staticmethod
    def fire_audio_tasks():
        atasks = list(filter(lambda x: x['type'] == Queue.AUDIO, Queue.queue))
        ar = AudioRequester()
        tasks_to_delete = []
        for i, task in atasks:
            if task['request'].method == 'POST':
                _, code = ar.post_audio(task['request'], task['data'])
            elif task['request'].method == 'PATCH':
                _, code = ar.patch_audio(task['request'], task['uuid'], task['data'])
            elif task['request'].method == 'DELETE':
                _, code = ar.delete_audio(task['request'], task['uuid'])
            else:
                code = 501
            if code < 500:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            Queue.queue.remove(task)

    @staticmethod
    def fire_image_tasks():
        itasks = list(filter(lambda x: x['type'] == Queue.IMAGE, Queue.queue))
        ir = ImagesRequester()
        tasks_to_delete = []
        for task in itasks:
            if task['request'].method == 'POST':
                _, code = ir.post_image(task['request'], task['data'])
            elif task['request'].method == 'PATCH':
                _, code = ir.patch_image(task['request'], task['uuid'], task['data'])
            elif task['request'].method == 'DELETE':
                _, code = ir.delete_image(task['request'], task['uuid'])
            else:
                code = 501
            if code < 500:
                tasks_to_delete.append(task)
        for task in tasks_to_delete:
            Queue.queue.remove(task)
