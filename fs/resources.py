import os  # do not need it anymore if I use Path to handle path
import hashlib
from pathlib import Path
from flask_restful import Resource
from flask import request, jsonify



class Uploader(Resource):

    def hasher(self, file_obj):
        BLOCK_SIZE = 65536 #64Kb
        file_hash = hashlib.sha256() 
        fb = file_obj.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = file_obj.read(BLOCK_SIZE)
        file_obj.seek(0)
        print('HASH!!!111', file_hash.hexdigest())
        return file_hash.hexdigest()



        # with open(filename, 'rb') as f:
        #     fb = f.read(BLOCK_SIZE)
        #     while len(fb) > 0:
        #         file_hash.update(fb)
        #         fb = f.read(BLOCK_SIZE)
        
        # print('HASH!!!111', file_hash.hexdigest())
        # return file_hash.hexdigest()


    def __init__(self, filedir):
        self.filedir = filedir

    def post(self):
        # curl -X POST 127.0.0.1:4000/api/upload -F 'file=@testfiles/test.txt' -i
        
        if request.files['file']:
            # TODO - write the original file name into log

            directory = self.filedir

            submitted_file = request.files['file']
            # submitted_file_name = submitted_file.filename

            submitted_file_name = self.hasher(submitted_file)

            submitted_file.save(Path(self.filedir) / submitted_file_name)
            out = {
                'status': 'OK',
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



