from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

# create an empty instance, later initiated in inisde create_app()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()