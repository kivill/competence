from orator import Model
from orator.orm import belongs_to, has_many


class ConfirmationFile(Model):
    __table__ = 'confirmation_files'

    __timestamps__ = ['created_at', 'updated_at']

    __fillable__ = [
        'confirmation_id',
        'file_url'
    ]

    @belongs_to('user_id')
    def user(self):
        from app.models.confirmation import Confirmation
        return Confirmation
