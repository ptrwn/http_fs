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
# app.logger.info('Processing default request') 

from fs.resources import Uploader
api.add_resource(Uploader, '/api/upload', endpoint='uploader', \
    resource_class_kwargs={'filedir': filedir})

from fs.resources import File
api.add_resource(File, '/api/file/<file_name>', endpoint='file', \
    resource_class_kwargs={'filedir': filedir})
