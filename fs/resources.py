from flask_restful import Resource


class Uploader(Resource):

    def post(self):
        print('got post')

    
    def put(self):
        print('got put')


class Downloader(Resource):
    pass


class Deleter(Resource):
    pass



