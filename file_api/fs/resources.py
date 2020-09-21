import hashlib
from pathlib import Path
from flask_restful import Resource
from flask import request, jsonify, send_from_directory, send_file, make_response
import logging

# Create logger object for generic messages.
logger = logging.getLogger(__name__)

# Create separate logger objects for Uploader and File resources
# to mark entries from each resource.
logUploader = logging.getLogger(__name__ + '.Uploader')
logFile = logging.getLogger(__name__ + '.File')

class Uploader(Resource):
    '''Resourse class that handles file uploads.

    Attributes:
        filedir - name of directory where files are stored. The name is set as
        config property UPLOAD_FOLDER, then passed from application __init__ when
        resource is added. 


    Methods:
        hasher - makes file hash, hash is then used as file name.

        saver - ensures that file sub-dir exists and saves file. 

        post - processes POST request to APT.

        put - TBD - to handle PUT request to API.
    '''

    def __init__(self, filedir):
        '''Get upload directory name from app __init__ .'''
        self.filedir = filedir

    def hasher(self, file_obj):
        '''Get file object from post function, return file hash to saver function.
        Blake2b was chosen as secure and fast hashing algorithm.
        '''

        BLOCK_SIZE = 65536 #64Kb
        file_hash = hashlib.blake2b() 
        fb = file_obj.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = file_obj.read(BLOCK_SIZE)
        file_obj.seek(0)
        return file_hash.hexdigest()


    def saver(self, file_obj, file_name):
        '''Get file object from post and file hash from hasher.
        Check that sub-directory for new file exists, otherwise create.
        '''

        subdir_name = file_name[0:2]
        subdir_path = Path(self.filedir) / subdir_name

        if not (subdir_path.exists() and subdir_path.is_dir()):
            Path(subdir_path).mkdir()
            logUploader.info(f'Subdir {subdir_path} created.')
        
        file_obj.save(Path(subdir_path) / file_name)
        logUploader.info(f'File {file_name} saved.')

        # TODO: handle failures of subdir creation or file saving:
        # permissions, disk full, file already exists with dir name, ...

        out = {
            'status': 'OK',
            'path': str(Path(subdir_path)),
            'filename': file_name,
            'message': f"{file_name} saved successfully."
            }

        return jsonify(out)



    def post(self):
        '''Handle files submitted with POST request, for example:
        curl -X POST 127.0.0.1:4000/api/upload -F 'file=@testfiles/test.txt' -i

        File hashing and saving are handled in corresponding functions. 
        Response returns status, new file name and subdir name.
        '''
        
        if request.files['file']:
            submitted_file = request.files['file']
            logUploader.info(f'File received, original name: {submitted_file.filename}.')
            submitted_file_name = self.hasher(submitted_file)
            
            return self.saver(submitted_file, submitted_file_name)
   
    def put(self):
        # curl --upload-file 'testfiles/test.txt' 127.0.0.1:4000/api/upload
        # TODO: add logic to handle files sent via put request ^
        pass


class File(Resource):
    '''Resourse class that handles file download and delete.

    Attributes:
        filedir - name of directory where files are stored. The name is set as
        config property UPLOAD_FOLDER, then passed from application __init__ when
        resource is added. 


    Methods:
        search - search for an existing file for download (GET) or DELETE.

        get - return file by its hash.

        delete - delete file by its hash.
    '''

    def __init__(self, filedir):
        '''Get upload directory name from app __init__ .'''
        self.filedir = filedir

    def search(self, file_name):
        '''Search for file by its hash by checking existence of full path. 
        Return file path and name or error that file is not found.        
        '''
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
        '''Return file to user by file hash, example of request:
        curl 127.0.0.1:4000/api/file/hash_of_required_file --output resulting.file

        send_from_directory function was chosen as more secure than send_file,
        as it send file only from speficied location.        
        '''
        
        logFile.info(f'Received GET request for file, name: {file_name}')
        search_result = self.search(file_name)

        if search_result.get('error', None):
            return make_response(jsonify(search_result), 404)
        else:
            logFile.info(f'Sent file: {file_name}')
            return send_from_directory(search_result['subdir'], 
                                        search_result['name'])


    def delete(self, file_name):
        '''Delete file by its hash, example of request:
        curl -X DELETE 127.0.0.1:4000/api/file/hash_of_required_file

        If sub-directroty remains empty after file is deleted, it will be 
        deleted as well.
        '''        

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
