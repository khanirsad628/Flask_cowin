from flask import Flask
from cowin_APP.config import Config
from cowin_APP.main.routes import main
from cowin_APP.errors.handlers  import errors
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app

from cowin_APP.main.routes import main
from cowin_APP.main import routes
from cowin_APP.errors.handlers  import errors
