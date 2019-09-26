from TestUtils.models import BaseTestCase
from MessagesApp.models import Message


class AllMessagesTestCase(BaseTestCase):
    """
    Тест для получения списка всех сообщений
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'messages/all/'
        self.message, _ = Message.objects.get_or_create(
            from_user_id=1,
            to_user_id=1,
            text='Text'
        )

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(len(response), 1)
        msg = response[0]
        self.assertEqual(msg['text'], self.message.text)
        self.assertEqual(msg['uuid'], str(self.message.uuid))


class MessagesTestCase(BaseTestCase):
    """
    Тест ендпоинта api/messages/<user_id>/
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
        self.url_404 = self.url_prefix + f'messages/0/'
        self.url_200 = self.url_prefix + f'messages/{self.message1.to_user_id}/'

    def testGet404(self):
        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet200(self):
        response = self.get_response_and_check_status(url=self.url_200)
        self.assertEqual(len(response), 2)
