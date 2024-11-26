from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)

    # Select the configuration class based on the config_name
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        raise ValueError(f"Unknown configuration: {config_name}")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app,db)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify the login route
    
    @app.context_processor
    def inject_year():
        return dict(current_year=datetime.utcnow().year)

    # Register blueprints (e.g., auth, accounts, etc.)
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.accounts.routes import accounts_bp
    from app.transactions.routes import transactions_bp
    
    app.register_blueprint(main_bp)  # Main blueprint for the home route
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    return app