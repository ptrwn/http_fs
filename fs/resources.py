import os  # do not need it anymore if I use Path to handle path
import hashlib
from pathlib import Path
from flask_restful import Resource
from flask import request, jsonify



class Uploader(Resource):

    def __init__(self, filedir):
        self.filedir = filedir

    def hasher(self, file_obj):

        BLOCK_SIZE = 65536 #64Kb
        file_hash = hashlib.sha256() 
        fb = file_obj.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = file_obj.read(BLOCK_SIZE)
        file_obj.seek(0)
        return file_hash.hexdigest()


    def saver(self, file_obj):
        pass



    def post(self):
        # curl -X POST 127.0.0.1:4000/api/upload -F 'file=@testfiles/test.txt' -i
        
        if request.files['file']:
            # TODO - write the original file name into log

            directory = self.filedir

            submitted_file = request.files['file']
            # submitted_file_name = submitted_file.filename

            submitted_file_name = self.hasher(submitted_file)
            # submitted_file_name = '71submitted_1cf311a8ce4d57289d6faa93d0c43809a8b5b14f9b9d66f013af'

            subdir_name = submitted_file_name[0:2]
            subdir_path = Path(self.filedir) / subdir_name
            if not (subdir_path.exists() and subdir_path.is_dir()):
                Path(subdir_path).mkdir()
            
            submitted_file.save(Path(subdir_path) / submitted_file_name)
            out = {
                'status': 'OK',
                'path': str(Path(subdir_path)),
                'filename': submitted_file_name,
                'message': f"{submitted_file_name} saved successful."
                }

            return jsonify(out)


    
    def put(self):
        # curl --upload-file 'testfiles/test.txt' 127.0.0.1:4000/api/upload
        print('got put')


class Downloader(Resource):
    pass


class Deleter(Resource):
    pass



