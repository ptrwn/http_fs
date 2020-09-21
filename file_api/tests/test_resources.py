import os, unittest
from fs import app
from fs.resources import Uploader, File
from io import BytesIO
from flask import url_for
from pathlib import Path
import shutil


class SetupTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_mode_is_on(self):
        self.assertEqual(self.app.application.config['UPLOAD_FOLDER'], 'test_store')
        self.assertTrue(self.app.application.config['TESTING'] is True)
        self.assertTrue(self.app.application.config['DEBUG'] is False)


class ResTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
       
    def test_upload(self):

        data = {'file': (BytesIO(b"f3123123file"), 'utest_file.txt'), }

        response = self.app.post(
            '/api/upload', data=data,
            follow_redirects=True,
            content_type='multipart/form-data'
        )
        self.assertIn(b'saved successfully.', response.data)

    def tearDown(self):
        path = Path(__file__).parent.parent / (app.config['UPLOAD_FOLDER'])
        shutil.rmtree(path)


if __name__ == '__main__':
    unittest.main()