from flask import Flask

from app.extensions import cache, db
from app.logger import configure_logger
from app.utils import initialize_db_with_json_data
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_logger(app)

    # Initialize Flask extensions here

    # SQLAlchemy
    db.init_app(app)
    with app.app_context():
        initialize_db_with_json_data()

    # Flask-Caching
    cache.init_app(app)

    # Register blueprints here
    from app.blueprints.events import bp as events_bp
    from app.blueprints.skills import bp as skills_bp
    from app.blueprints.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(skills_bp, url_prefix='/skills')
    app.register_blueprint(events_bp, url_prefix='/events')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application</h1>'

    return app
