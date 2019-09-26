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
