import uuid
from TestUtils.models import BaseTestCase
from ImagesApp.models import Image


class ImagesListTestCase(BaseTestCase):
    """
    Тест ендпоинта /api/images/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'images/'
        self.image1, _ = Image.objects.get_or_create(name='test1.jpg', width=300, height=300)
        self.image2, _ = Image.objects.get_or_create(name='test2.jpg.psd', width=100, height=100)
        self.data_400 = {
            'nam': 'no',
        }
        self.data_201 = {
            'name': 'post',
            'width': 300,
            'height': 300,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        # Длинна массива
        self.assertEqual(len(response), 2)
        # UUID
        self.assertEqual(response[0]['uuid'], str(self.image1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.image2.uuid))
        # Правильно рассчитывает расширение
        self.assertEqual(response[0]['extension'], 'jpg')
        self.assertEqual(response[1]['extension'], 'psd')
        # Правильно прислал расширение
        self.assertEqual(response[0]['extension'], self.image1.extension)
        self.assertEqual(response[1]['extension'], self.image2.extension)
        # Правильно выдает размер
        self.assertEqual(response[0]['image_size'], f'{self.image1.width}x{self.image1.height}')

    def testPost400(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost201(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = Image.objects.get(pk=response['uuid'])
        except Image.DoesNotExist:
            self.assertTrue(False)
            return  # Чтобы идеха не выделяла new ниже желтым
        self.assertEqual(new.name, self.data_201['name'])
        self.assertEqual(new.width, self.data_201['width'])
        self.assertEqual(new.height, self.data_201['height'])


class ConcreteImageViewTestCase(BaseTestCase):
    """
    Тесты для ендпоинта /api/images/<image_uuid>/
    """
    def setUp(self):
        super().setUp()
        self.image, _ = Image.objects.get_or_create(name='test', width=300, height=300)
        uuid_tmp = uuid.uuid4()
        self.url_404 = self.url_prefix + f'images/{uuid_tmp}/'
        while uuid_tmp == self.image.uuid:
            uuid_tmp = uuid.uuid4()
            self.url_404 = self.url_prefix + f'images/{uuid_tmp}/'
        self.url = self.url_prefix + f'images/{self.image.uuid}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(response['uuid'], str(self.image.uuid))
        self.assertEqual(response['name'], self.image.name)
        self.assertEqual(response['image_size'], self.image.image_size)

    def testDelete(self):
        _ = self.delete_response_and_check_status(url=self.url, expected_status_code=204)
        self.assertEqual(Image.objects.count(), 0)
