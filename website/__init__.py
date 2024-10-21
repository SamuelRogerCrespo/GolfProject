from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()  # Initialize Flask-Migrate

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Check if the app is running in Heroku by checking for the 'DATABASE_URL' environment variable
    if os.environ.get('DATABASE_URL'):
        # Heroku uses PostgreSQL
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    else:
        # Local development uses SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)  # Bind Flask-Migrate to the app

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        # Create the instance folder if it does not exist
        if not os.path.exists('instance'):
            os.makedirs('instance')

        # If SQLite, create the database file if it does not exist
        if not os.path.exists(f'instance/{DB_NAME}'):
            db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
