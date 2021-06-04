import random
from orator.seeds import Seeder
from orator.orm import Factory
from app.models.school import School
from app.models.user import User
import uuid

factory = Factory()


@factory.define(School)
def school_factory(faker):
    return {
        'name': faker.company(),
        'address': faker.street_address(),
    }


@factory.define(User)
def users_factory(faker):
    return {
        'full_name': faker.name(),
        'email': faker.email(),
        'password': faker.password(length=12),
        'role': 'учитель',
        'uuid': str(uuid.uuid4())
    }


@factory.define(User, 'admin')
def admin_users_factory(faker):
    user = factory.raw(User)

    user.update({
        'role': 'директор',
    })

    return user


@factory.define(User, 'metodist')
def metodist_users_factory(faker):
    user = factory.raw(User)

    user.update({
        'role': 'методист',
    })

    return user


class SchoolTableSeeder(Seeder):

    factory = factory

    def run(self):
        """
        Run the database seeds.
        """
        school = self.factory(School).create()
        school.users().save(self.factory(User, 'admin').make())
        school.users().save(self.factory(User, 'metodist').make())
        school.users().save_many(
            self.factory(User, 30).make())
