import unittest
from main import app


class MyTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/search.html")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # Ensure that page is in search bar screen
    def test_search_bar_is_in_screen(self):
        tester = app.test_client(self)
        response = tester.get("/search.html")
        self.assertIn(b'Search...', response.data)
        self.assertNotIn(b'Item not in database', response.data)
        self.assertNotIn(b'stock', response.data)

    # Ensure that page works when data searched is not in database
    def test_info_searched_not_in_database(self):
        tester = app.test_client(self)
        response = tester.post('/search.html', data=dict(search_input='test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Item not in database', response.data)
        self.assertNotIn(b'stock', response.data)
        self.assertNotIn(b'Search...', response.data)

    # Ensure that page works when data searched is in database
    def test_info_searched_is_in_database(self):
        tester = app.test_client(self)
        response = tester.post('/search.html', data=dict(search_input='Nex'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Nex', response.data)
        self.assertTrue(b'Stock', response.data)
        self.assertNotIn(b'Item not in database', response.data)
        self.assertNotIn(b'Search...', response.data)


if __name__ == '__main__':
    unittest.main()
