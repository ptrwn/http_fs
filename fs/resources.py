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


    def saver(self, file_obj, file_name):

        subdir_name = file_name[0:2]
        subdir_path = Path(self.filedir) / subdir_name

        if not (subdir_path.exists() and subdir_path.is_dir()):
            Path(subdir_path).mkdir()
        
        file_obj.save(Path(subdir_path) / file_name)

        out = {
            'status': 'OK',
            'path': str(Path(subdir_path)),
            'filename': file_name,
            'message': f"{file_name} saved successfully."
            }

        print(out)

        return jsonify(out)



    def post(self):
        # curl -X POST 127.0.0.1:4000/api/upload -F 'file=@testfiles/test.txt' -i
        
        if request.files['file']:
            # TODO - write the original file name into log
            # submitted_file_name = submitted_file.filename

            directory = self.filedir
            submitted_file = request.files['file']
            submitted_file_name = self.hasher(submitted_file)            
            self.saver(submitted_file, submitted_file_name)

    
    def put(self):
        # curl --upload-file 'testfiles/test.txt' 127.0.0.1:4000/api/upload
        print('got put')


class File(Resource):

    def __init__(self, filedir):
        self.filedir = filedir

    def search(self):
        pass

    def get(self, file_name):
        print('GOT THIS', file_name)

        subdir_name = file_name[0:2]
        subdir_path = Path(self.filedir) / subdir_name

        if not subdir_path.exists():
            return jsonify({'error':'file does not exist'})

    def delete(self):
        pass
    

        




