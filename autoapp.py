import os
from flaskdeliveryapp import create_app, db
from flaskdeliveryapp.user.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flaskdeliveryapp.app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def db_setup():
    """Set up the database"""
    Role.insert_roles()
    Tag.insert_tags()

@manager.command
def reset_db():
    """Empties the database and generates it again with db_setup"""
    db.drop_all()
    db.create_all()
    db_setup()

@manager.command
def reset_database():
    """Setup the database."""
    from flask_migrate import upgrade
    from subprocess import call

    # Reset the database
    call(['sudo', 'service', 'rh-postgresql95-postgresql', 'restart'])
    call(['sudo', '-u', 'postgres', '/opt/rh/rh-postgresql95/root/usr/bin/dropdb', 'flaskdeliveryapp'])
    call(['sudo', '-u', 'postgres', '/opt/rh/rh-postgresql95/root/usr/bin/createdb', 'flaskdeliveryapp'])

    # Run migrations
    upgrade()

    # pre-populate
    list(
        map(
            lambda x: x.populate(),
            (
                Roles,
                Users
            )
        )
    )


@manager.command
def deploy():
    """Upgrade and pre-populate database"""
    from flask_migrate import upgrade
    # Run migrations
    upgrade()

    # pre-populate
    list(
        map(
            lambda x: x.populate(),
            (
                Roles,
                Users
            )
        )
    )


if __name__ == '__main__':
    manager.run()

