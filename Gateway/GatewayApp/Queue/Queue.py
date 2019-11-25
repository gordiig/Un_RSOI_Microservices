from typing import Union


class Queue:
    AUDIO, IMAGE = 'audio', 'image'
    _audio_status, _image_status = 1, 1
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
        Queue._image_status = 0
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.IMAGE)
        print('Add image task to queue')

    @staticmethod
    def add_audio_task(request, data: Union[None, dict] = None, uuid: Union[None, str] = None):
        Queue._audio_status = 0
        Queue._add_task_to_queue(request, data, uuid, ttype=Queue.AUDIO)
        print('Add audio task to queue')

    @staticmethod
    def fire_audio_tasks():
        from GatewayApp.requesters.audio_requester import AudioRequester
        if Queue._audio_status == 1:
            return
        else:
            Queue._audio_status = 1
        print('Firing audio tasks...')
        atasks = list(filter(lambda x: x['type'] == Queue.AUDIO, Queue.queue))
        ar = AudioRequester()
        tasks_to_delete = []
        for task in atasks:
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
        print(f'{len(tasks_to_delete)} audio tasks fired with success')

    @staticmethod
    def fire_image_tasks():
        from GatewayApp.requesters.images_requester import ImagesRequester
        if Queue._image_status == 1:
            return
        else:
            Queue._image_status = 1
        print('Firing image tasks...')
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
        print(f'{len(tasks_to_delete)} image tasks fired with success')
