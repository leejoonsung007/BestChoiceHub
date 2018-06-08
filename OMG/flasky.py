import os
from flask_migrate import Migrate
from app import create_app
from app.models import *
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


# @app.cli.command()
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


#测试一下数据库迁移文件是否能够正常使用
# set FLASK_APP=flasky.py
# flask db upgrade
# 看看是table是否能创建出来
