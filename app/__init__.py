import os
import logging
from flask import Flask
from app.config import config_by_name
from app.extensions import db, login_manager, csrf


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # bind extensions to this app instance
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # import models so SQLAlchemy knows about them before create_all()
    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # register blueprints
    from app.auth.routes import auth_bp
    from app.recipes.routes import recipes_bp
    from app.main.routes import main_bp
    from app.profile.routes import profile_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    # configure logging
    configure_logging(app)

    # create tables + upload folder if they don't exist
    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(app.root_path), 'instance'), exist_ok=True)
        db.create_all()

    # error handlers
    register_error_handlers(app)

    return app


def configure_logging(app):
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app.logger.info('Recipe app startup')


def register_error_handlers(app):
    from flask import render_template

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403


    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return render_template('errors/500.html'), 500