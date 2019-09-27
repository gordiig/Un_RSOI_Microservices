import uuid
from TestUtils.models import BaseTestCase
from AudioApp.models import Audio


class AudiosViewTestCase(BaseTestCase):
    """
    Тесты для ендпоинта /api/audio/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'audio/'
        self.audio1, _ = Audio.objects.get_or_create(name='test1', length=60)
        self.audio2, _ = Audio.objects.get_or_create(name='test2', length=120)
        self.data_400 = {
            'na': 'no',
        }
        self.data_201 = {
            'name': 'post',
            'length': 180,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        # Количество объектов в ответе
        self.assertEqual(len(response), 2)
        # UUID
        self.assertEqual(response[0]['uuid'], str(self.audio1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.audio2.uuid))
        # Правильность остальных данных
        self.assertEqual(response[0]['name'], self.audio1.name)
        self.assertEqual(response[1]['name'], self.audio2.name)
        self.assertEqual(response[0]['length'], self.audio1.length)
        self.assertEqual(response[1]['length'], self.audio2.length)

    def testPost400(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = Audio.objects.get(pk=response['uuid'])
        except Audio.DoesNotExist:
            self.assertTrue(False)
            return  # Чтобы идеха не подсвечивала new желтым ниже
        self.assertEqual(new.name, self.data_201['name'])
        self.assertEqual(new.length, self.data_201['length'])


