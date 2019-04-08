from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from config import Config
from .db import db

login_manager = LoginManager()
login_manager.login_view = 'main.home'

def create_app(config=Config):

	app = Flask(__name__)

	app.config.from_object(config)

	login_manager.init_app(app)
	db.init()

	from .auth import bp as auth_bp
	app.register_blueprint(auth_bp)

	from .main import bp as main_bp
	app.register_blueprint(main_bp)

	return app
