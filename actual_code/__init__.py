from flask import Flask
from .extensions import db, login_manager
from .routes import main
from .models import User,Admin
from .commands import create_tables

def create_app(config_file='settings.py'):
    app= Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view= 'main.login'
    @login_manager.user_loader
    def load_user(id):
        user = Admin.query.get(id)
        return user


    app.register_blueprint(main)
    app.cli.add_command(create_tables)

    return app
