import rq
from redis import Redis
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_orator import Orator
from flask_session import Session
from flask_jwt_extended import JWTManager

from pymemcache.client import base

from app.configs.application import config


class FlaskApplication:
    def __init__(self):
        self.static_folder = '../public/dist/'
        self.app = Flask(__name__, static_folder=self.static_folder)

        self.app.config.update(config)

        self.__route_list = []
        self.__cors_instance = CORS()
        self.__jwt_instance = JWTManager()
        self.__orator_instance = Orator()
        self.__bcrypt_instance = Bcrypt()
        self.__session_instance = Session()

    @property
    def db(self):
        return self.__orator_instance

    @property
    def jwt(self):
        return self.__jwt_instance

    @property
    def bcrypt(self):
        return self.__bcrypt_instance

    def __unpack_routes(self, routes=None, prefix=''):

        if not routes:
            from app.routes import ROUTES
            routes = ROUTES

        for route in routes:
            route_prefix = prefix + route.get('prefix', '')
            if route.get('group'):
                self.__unpack_routes(routes=route.get(
                    'group'), prefix=route_prefix)
            if route.get('controller'):
                self.__route_list.append({
                    'blueprint': route['controller'],
                    'url_prefix': route_prefix
                })

    def __register_blueprints(self):
        for route in self.__route_list:
            self.app.register_blueprint(**route)

    def init(self):
        self.__cors_instance.init_app(self.app)
        self.__jwt_instance.init_app(self.app)
        self.__orator_instance.init_app(self.app)
        self.__bcrypt_instance.init_app(self.app)
        self.__session_instance.init_app(self.app)

        self.__unpack_routes()
        self.__register_blueprints()

        return self.app
