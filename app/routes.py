from app.controllers.user_controller import UserController
from app.controllers.school_controller import SchoolController
from app.controllers.course_controller import CourseController

ROUTES = [
    {
        'prefix': '/api',
        'group': [
            {'prefix': '/user', 'controller':  UserController},
            {'prefix': '/school', 'controller':  SchoolController},
            {'prefix': '/course', 'controller':  CourseController},
        ]
    }
]
