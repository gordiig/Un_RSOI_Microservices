import uuid
from TestUtils.models import BaseTestCase
from MessagesApp.models import Message


class AllMessagesTestCase(BaseTestCase):
    """
    Тест для получения списка всех сообщений
    """
    def setUp(self):
        super().setUp()
        self.message1, _ = Message.objects.get_or_create(
            from_user_id=1,
            to_user_id=2,
            text='Text'
        )
        self.message2, _ = Message.objects.get_or_create(
            from_user_id=2,
            to_user_id=3,
            text='Text2'
        )
        self.url_404 = self.url_prefix + 'messages/?user_id=0'
        self.url_200 = self.url_prefix + f'messages/?user_id={self.message1.to_user_id}'

    def testGet404(self):
        msgs = self.get_response_and_check_status(url=self.url_404, expected_status_code=200)
        self.assertEqual(len(msgs), 0)


    def testGet200(self):
        response = self.get_response_and_check_status(url=self.url_200)
        self.assertEqual(len(response), 2)


class ConcreteMessageTestCase(BaseTestCase):
    """
    Тесты для ендпоинта api/messages/<message:id>/
    """
    def setUp(self):
        super().setUp()
        self.message1, _ = Message.objects.get_or_create(
            from_user_id=1,
            to_user_id=2,
            text='Text'
        )
        self.message2, _ = Message.objects.get_or_create(
            from_user_id=2,
            to_user_id=3,
            text='Text2'
        )
        uuid_404 = uuid.uuid4()
        while uuid_404 in (self.message1.uuid, self.message2.uuid):
            uuid_404 = uuid.uuid4()
        self.url_404 = self.url_prefix + f'messages/{str(uuid_404)}/'
        self.url_200 = self.url_prefix + f'messages/{self.message1.uuid}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet200(self):
        response = self.get_response_and_check_status(url=self.url_200)
        self.assertEqual(response['uuid'], str(self.message1.uuid))

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete204(self):
        _ = self.delete_response_and_check_status(url=self.url_200, expected_status_code=204)
