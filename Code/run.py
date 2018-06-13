import os
from flask_migrate import Migrate
from app import create_app
from app import db
from app.models.Roleomg import Role
from app.models.User import User
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


if __name__ == '__main__':
    app.run(debug=True)
