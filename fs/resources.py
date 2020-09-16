import hashlib
from pathlib import Path
from flask_restful import Resource
from flask import request, jsonify, send_from_directory, send_file, make_response


import logging
logger = logging.getLogger(__name__)
logUploader = logging.getLogger(__name__ + '.Uploader')
logFile = logging.getLogger(__name__ + '.File')

class Uploader(Resource):

    def __init__(self, filedir):
        self.filedir = filedir

    def hasher(self, file_obj):

        BLOCK_SIZE = 65536 #64Kb
        file_hash = hashlib.blake2b() 
        fb = file_obj.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = file_obj.read(BLOCK_SIZE)
        file_obj.seek(0)
        return file_hash.hexdigest()


    def saver(self, file_obj, file_name):

        subdir_name = file_name[0:2]
        subdir_path = Path(self.filedir) / subdir_name

        if not (subdir_path.exists() and subdir_path.is_dir()):
            Path(subdir_path).mkdir()
            logUploader.info(f'Subdir {subdir_path} created.')
        
        file_obj.save(Path(subdir_path) / file_name)
        logUploader.info(f'File {file_name} saved.')

        out = {
            'status': 'OK',
            'path': str(Path(subdir_path)),
            'filename': file_name,
            'message': f"{file_name} saved successfully."
            }

        return jsonify(out)



    def post(self):
        # curl -X POST 127.0.0.1:4000/api/upload -F 'file=@testfiles/test.txt' -i
        
        if request.files['file']:
            directory = self.filedir
            submitted_file = request.files['file']
            logUploader.info(f'File received, original name: {submitted_file.filename}.')
            submitted_file_name = self.hasher(submitted_file)
            
            return self.saver(submitted_file, submitted_file_name)
   
    def put(self):
        # curl --upload-file 'testfiles/test.txt' 127.0.0.1:4000/api/upload
        print('got put')


class File(Resource):

    def __init__(self, filedir):
        self.filedir = filedir

    def search(self, file_name):
        subdir_name = file_name[0:2]
        file_path = Path(self.filedir) / subdir_name / file_name
        file_subdir = Path(self.filedir) / subdir_name

        if not file_path.exists():
            logFile.info(f'File not found: {file_name}')
            return {'error':'file does not exist'}
        else:
            return {'subdir': file_subdir,
                    'name': file_name,}


    def get(self, file_name):
        # curl 127.0.0.1:4000/api/file/somefile.txt --output some.file
        
        logFile.info(f'Received GET request for file, name: {file_name}')
        search_result = self.search(file_name)

        if search_result.get('error', None):
            return make_response(jsonify(search_result), 404)
        else:
            logFile.info(f'Sent file: {file_name}')
            return send_from_directory(search_result['subdir'], 
                                        search_result['name'])


    def delete(self, file_name):
        # curl -X DELETE 127.0.0.1:4000/api/file/test.txt

        logFile.info(f'Received DELETE request for file, name: {file_name}')
        search_result = self.search(file_name)

        if search_result.get('error', None):
            return make_response(jsonify(search_result), 404)
        else:
            file_subdir = search_result['subdir']
            file_name = search_result['name']
            Path.unlink(file_subdir / file_name)
            logFile.info(f'Deleted file: {file_name}')
            out = {
            'status': 'OK',
            'filename': file_name,
            'message': f"File {file_name} deleted successfully."
            }
            is_empty = not any(Path(file_subdir).iterdir())
            if is_empty:
                Path.rmdir(file_subdir)
                logFile.info(f'Deleted folder: {file_subdir}')
                out['path'] = str(file_subdir)
                out['message_dir'] = f"Folder {file_subdir} deleted successfully."
               
            return jsonify(out)
