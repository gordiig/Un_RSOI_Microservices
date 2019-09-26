from TestUtils.models import BaseTestCase


class RegisterTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'register/'
        self.data_201 = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com',
        }
        self.data_empty = {

        }
        self.data_400 = {
            'username': 'tt',
        }

    def testOk(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            self.assertEqual(response['username'], self.data_201['username'])
            self.assertEqual(response['email'], self.data_201['email'])
            self.assertTrue(response['id'] is not None)
        except KeyError:
            self.assertTrue(False, msg='Key error')

    def testEmpty(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_empty, expected_status_code=400)

    def testWrong(self):
        _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)
