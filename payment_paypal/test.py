import unittest

import __init

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app =  __init.

    def test_main_page(self):
        response = self.app.get('/purchase/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()       
        