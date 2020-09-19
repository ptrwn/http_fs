import unittest
from fs import app
from fs.resources import Uploader, File
from io import BytesIO
from flask import url_for

from pathlib import Path


class ResTest(unittest.TestCase):

    def setUp(self):
        
        #app.config['DEBUG'] = False
        app.config.update(
            TESTING=True,
            UPLOAD_FOLDER = 'test_store'            
            )

    def test_upload(self):

        data = {'file': (BytesIO(b"file file 111 file"), 'utest_file.txt'), }

        client = app.test_client()

        response = client.post(
            '/api/upload', data=data,
            follow_redirects=True,
            content_type='multipart/form-data'
        )
        self.assertIn(b'saved successfully.', response.data)

    # def test_download(self):
    #     pass

    # def test_delete(self):
    #     pass


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()