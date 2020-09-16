from pathlib import Path
from flask import Flask
from flask_restful import Api

import logging.handlers
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "fs.log"))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)
logger.info('App initiated.')

# export FLASK_ENV variable to production or development
if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.Config")
    logger.debug('Production config loaded.')
else:
    app.config.from_object("config.DevConfig")
    logger.debug('Development config loaded.')

filedir = Path(__file__).parent.parent / (app.config['UPLOAD_FOLDER'])

# verify that upload directory exists:
if not (filedir.exists() and filedir.is_dir()):
    try:
        Path(filedir).mkdir()
        logger.info('Upload folder created.')
    except FileExistsError:
        err_message = f"File named \"{app.config['UPLOAD_FOLDER']}\" already exists. Rename the file or set a different name for the upload folder in config.py."
        logger.critical("Exception. " + err_message)
        raise Exception(err_message)


api = Api(app)

from fs.resources import Uploader
api.add_resource(Uploader, '/api/upload', endpoint='uploader', \
    resource_class_kwargs={'filedir': filedir})

from fs.resources import File
api.add_resource(File, '/api/file/<file_name>', endpoint='file', \
    resource_class_kwargs={'filedir': filedir})