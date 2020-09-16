class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'store'


class DevConfig(Config):
    DEBUG = True


