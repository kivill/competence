from orator import Model
from orator.orm import belongs_to, has_many, belongs_to_many, has_many_through
from app.models.confirmation import Confirmation
from app.models.cource import Cource

class Competence(Model):
    __table__ = 'competencies'

    __timestamps__ = ['created_at', 'updated_at']

    __fillable__ = [
        'name',
        'description',
    ]

    @belongs_to_many('courses_competencies', 'competencies_id', 'course_id')
    def cources(self):
        return Cource

    @has_many('competence_id')
    def confirmations(self):
        return Confirmation

    @has_many_through(Confirmation, 'competence_id', 'user_id')
    def users(self):
        from app.models.user import User
        return User
