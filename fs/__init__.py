from pathlib import Path
from flask import Flask
from flask_restful import Api

import logging.handlers
import logging
import os

'''Set up application.

- Logging.
- Selest config (production, development, or testing).
- Verify that folder for uploading files is accessible.
- Import API resources.

Create application object and api object. 

Raise:
    FileExistsError: The upload directory name is already taken by a file.
'''


# Create logger object.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Name of log file is taken from env variable LOGFILE, defaults to 
# fs.log if the variable was not set.
file_handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "fs.log"))
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)
logger.info('App initiated.')


# Before running the app, export FLASK_ENV variable to choose config.
if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.Config")
    logger.debug('Production config loaded.')
elif os.environ.get("FLASK_ENV") == "testing":
    app.config.from_object("config.TestConfig")
    logger.debug('Testing config loaded.')
else:
    app.config.from_object("config.DevConfig")
    logger.debug('Development config loaded.')
    

filedir = Path(__file__).parent.parent / (app.config['UPLOAD_FOLDER'])

# Verify that upload directory exists:
if not (filedir.exists() and filedir.is_dir()):
    try:
        # create, if it doesn't
        Path(filedir).mkdir()
        logger.info('Upload folder created.')
    except FileExistsError:
        # raise exception if dir name conflict with a file.
        err_message = f"File named \"{app.config['UPLOAD_FOLDER']}\" already exists. Rename the file or set a different name for the upload folder in config.py."
        logger.critical("Exception. " + err_message)
        raise FileExistsError(err_message)


api = Api(app)

# Import resource that handles file upload. Pass file storage dir
# to resource class.
from fs.resources import Uploader
api.add_resource(Uploader, '/api/upload', endpoint='uploader', \
    resource_class_kwargs={'filedir': filedir})

# Import resource that handles download and delete. Same URL is used 
# in both cases, action depends on HTTP method: GET for download,
# DELETE for delete.
from fs.resources import File
api.add_resource(File, '/api/file/<file_name>', endpoint='file', \
    resource_class_kwargs={'filedir': filedir})