import os
from pathlib import Path
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config.from_object("config.Config")
filedir = Path(__file__).parent.parent / (app.config['UPLOAD_FOLDER'])

if not (filedir.exists() and filedir.is_dir()):
    try:
        Path(filedir).mkdir()
    except FileExistsError:
        raise Exception(f"File named \"{app.config['UPLOAD_FOLDER']}\" already exists. \
            Rename the file or set a different name for the upload folder in config.py.")

api = Api(app)

from fs.resources import Uploader
api.add_resource(Uploader, '/api/upload', endpoint='uploader')

from fs.resources import Downloader
api.add_resource(Downloader, '/api/download', endpoint='downloader')

from fs.resources import Deleter
api.add_resource(Deleter, '/api/delete', endpoint='deleter')