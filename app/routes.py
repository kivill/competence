from app.controllers.user_controller import UserController
from app.controllers.school_controller import SchoolController
from app.controllers.course_controller import CourseController
from app.controllers.competence_controller import CompetenceController
from app.controllers.confirmation_controller import ConfirmationController

ROUTES = [
    {
        'prefix': '/api',
        'group': [
            {'prefix': '/user', 'controller':  UserController},
            {'prefix': '/school', 'controller':  SchoolController},
            {'prefix': '/course', 'controller':  CourseController},
            {'prefix': '/competence', 'controller':  CompetenceController},
            {'prefix': '/confirmation', 'controller':  ConfirmationController},
        ]
    }
]
