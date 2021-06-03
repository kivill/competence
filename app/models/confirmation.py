from orator import Model
from orator.orm import belongs_to, has_many


class Confirmation(Model):
    __table__ = 'confirmations'

    __timestamps__ = ['created_at', 'updated_at']

    __fillable__ = [
        'user_id',
        'competence_id',
        'status',
    ]

    @belongs_to('user_id')
    def user(self):
        from app.models.user import User
        return User

    @belongs_to('competence_id')
    def profile(self):
        from app.models.competence import Competence
        return Competence

    @has_many('confirmation_id')
    def confirmation_files(self):
        from app.models.confirmation_file import ConfirmationFile
        return ConfirmationFile
