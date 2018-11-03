"""
Main app root for the api endpoints
"""
from flask import Flask

from api.config.config import DevelopmentConfig, HostConfig
from database.database import DatabaseConnection
from api.routes import Urls


class Server:
    """
    Class contains methods to create a flask instance
    """
    app = None

    def create_app(self, env=None):
        self.app = Flask(__name__)
        self.app.config.update(env.__dict__ or {})
        Urls.generate(self.app)

        with self.app.app_context():
            database = DatabaseConnection()
            database.init_db(self.app)
        return self.app


APP = Server().create_app(env=DevelopmentConfig)

if __name__ == '__main__':
    APP.run(host=HostConfig.HOST, port=HostConfig.PORT)
