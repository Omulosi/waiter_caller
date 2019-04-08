from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from config import Config

login_manager = LoginManager()

def create_app(config=Config):

	app = Flask(__name__)

	app.config.from_object(config)

	login_manager.init_app(app)

	from .auth import bp as auth_bp
	app.register_blueprint(auth_bp)


	from .main import bp as main_bp
	app.register_blueprint(main_bp)

	return app
