from orator import Model
from orator.orm import belongs_to, has_many, has_many_through, belongs_to_many
from app.models.confirmation import Confirmation

class User(Model):
    __table__ = 'users'

    __timestamps__ = ['created_at', 'updated_at']

    __hidden__ = ['password']

    __fillable__ = [
        'school_id',
        'full_name',
        'email',
        'password',
        'position',
        'uuid',
    ]

    @belongs_to('school_id')
    def school(self):
        from app.models.school import School
        return School

    @has_many('user_id')
    def confirmations(self):
        return Confirmation

    @has_many_through(Confirmation, 'user_id', 'competence_id')
    def competencies(self):
        from app.models.competence import Competence
        return Competence

    @belongs_to_many('confirmations', 'user_id', 'competence_id')
    def competences(self):
        from app.models.confirmation import Confirmation
        return Confirmation

    def get_jwt_identity(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'position': self.position,
        }
