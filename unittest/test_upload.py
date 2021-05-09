import unittest
from app import app


class UploadTest(unittest.TestCase):


    #Ensure the Flask is functional

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/Upload_Image.html")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

if __name__ == '__main__':
    unittest.main()
