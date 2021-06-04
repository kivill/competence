from app.controllers.user_controller import UserController
from app.controllers.school_controller import SchoolController

ROUTES = [
    {
        'prefix': '/api',
        'group': [
            {'prefix': '/user', 'controller':  UserController},
            {'prefix': '/school', 'controller':  SchoolController},
        ]
    }
]
