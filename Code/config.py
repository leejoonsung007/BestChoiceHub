import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <schoolselectionie@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_MODERATOR = os.environ.get('MODERATOR')
    # FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    # POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE')
    # FLASKY_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    # FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    # FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")

    OAUTHLIB_RELAX_TOKEN_SCOPE = True
    OAUTHLIB_INSECURE_TRANSPORT = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/mysql'


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#         'mysql+pymysql://root:1234@localhost/school'
#
#
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'mysql+pymysql://root:1234@localhost/school'


config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}
