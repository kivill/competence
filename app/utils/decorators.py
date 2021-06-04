from functools import wraps
from flask import request, jsonify
from cerberus import Validator
from flask_jwt_extended import get_jwt_identity


def singleton(class_):
    """
    Implementation of Singleton pattern
    :param class_: wrapped class
    :return: wraps
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def schema_validation(schema):
    """
    Validate request fields by cerberus
    Wrap flask blueprint endpoints
    :param schema: Validation schema
    :return: wraps
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            data = {}
            if request.method in ['POST', 'PATCH', 'PUT']:
                data = request.get_json(force=True)
            elif request.method in ['GET', 'DELETE']:
                data = request.args.to_dict()

            v = Validator(schema)
            v.allow_unknown = True
            if v.validate(data):
                return function(*args, **kwargs)
            else:
                return jsonify({'errors': v.errors}), 400

        return wrapper
    return decorator


def admin_required(fn):
    """
    Check admin permissions on jwt identity
    Wrap flask blueprint endpoints
    :param fn:
    :return: wraps
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            return jsonify({'message': 'Permission denied'}), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


def role_required(*role_names):
    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            identity = get_jwt_identity()
            if not identity['role'] in role_names:
                return jsonify({'message': 'Permission denied'}), 403
            else:
                return view_function(*args, **kwargs)
        return decorator
    return wrapper


class cached_property(object):
    """
    Cache computed property in class instance

    :param func:
    :return: wraps
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result
