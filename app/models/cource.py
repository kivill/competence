from orator import Model
from orator.orm import belongs_to, has_many, belongs_to_many

class Cource(Model):
    __table__ = 'courses'

    __timestamps__ = ['created_at', 'updated_at']

    __fillable__ = [
        'name',
        'description',
        'start',
    ]


    @belongs_to_many('courses_competencies', 'course_id', 'competence_id')
    def competences(self):
        from app.models.competence import Competence
        return Competence
