from orator import Model
from orator.orm import belongs_to, has_many


class School(Model):
    __table__ = 'schools'

    __timestamps__ = ['created_at', 'updated_at']

    __fillable__ = [
        'name',
        'address',
    ]

    @has_many('school_id')
    def users(self):
        from app.models.user import User
        return User
