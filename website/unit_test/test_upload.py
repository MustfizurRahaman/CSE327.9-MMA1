import unittest
from app import app


class UploadTest(unittest.TestCase):


    #Ensure the Flask is functional

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/Upload_Image")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_image(self):
        tester = app.test_client(self)
        response = tester.get("/Upload_Image")
        self.assertIsNot(b'Prediction', response.data)
    def test_image_two(self):
        tester = app.test_client(self)
        response = tester.post('/Upload_Image', data=dict(image='static/img/hnapa.png'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()
