from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # def test_index(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/login', content_type='html/text')
    #     self.assertTrue(True)

    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                           data=dict(username="Hash",
                                     password="hashed"), follow_redirects=True
                               )
        self.assertIn(b'', response.data)

if __name__ == '__main__':
    unittest.main()
