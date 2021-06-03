import datetime
from os import environ

config = {
    'JWT_SECRET_KEY': environ.get('JWT_SECRET'),
    'MAX_CONTENT_LENGTH': 256 * 1024 * 1024,
    'JWT_ACCESS_TOKEN_EXPIRES': datetime.timedelta(days=30),
    'SESSION_TYPE': 'memcached',
    'ORATOR_DATABASES': {
        'pgsql': {
            'driver': environ.get('DB_DRIVER'),
            'host': environ.get('DB_HOST'),
            'database': environ.get('DB_NAME'),
            'user': environ.get('DB_USER'),
            'password': environ.get('DB_PASSWORD'),
            'prefix': '',
            "use_qmark": True
        }
    },
}