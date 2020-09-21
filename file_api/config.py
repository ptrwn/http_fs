class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = 'store'


class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    DEBUG = False
    UPLOAD_FOLDER = 'test_store'


