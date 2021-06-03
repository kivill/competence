from app.controllers.user_controller import UserController
from app.controllers.company_controller import CompanyController

ROUTES = [
    {
        'prefix': '/api',
        'group': [
            {'prefix': '/user', 'controller':  UserController},
            {'prefix': '/company', 'controller':  CompanyController},
        ]
    }
]
