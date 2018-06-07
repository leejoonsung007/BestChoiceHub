import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # get (A,B) 后面这个B是默认值，如果A为空的话
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <schoolselectionie@gmail.com>' #这里也需要改成你的邮箱
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_MODERATOR = os.environ.get('MODERATOR')
    # FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    # POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE')
    # FLASKY_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 这部分很好考虑的安全性 不让自己的邮箱和密码暴露在代码中 所以把这些信息存储到了
    # 环境变量中 通过os.environ.get来获取 这样就保证了安全性
    # 使用方法： 在pycharm下的terminal 输入
    # sudo ~/.bashrc
    # 然后追加信息：
    #export MAIL_USERNAME="你的邮箱"
    # export MAIL_PASSWORD="邮箱密码"
    # export FLASKY_ADMIN="你的邮箱"


    @staticmethod
    def init_app(app):
        pass

# 这里我们不需要这么高级的 还分开发环境 测试环境。。。所以改掉
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:1234@localhost/school'


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
# 配置和数据库的连接信息
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/school'
#SQLALCHEMY_TRACK_MODIFICATIONS = True