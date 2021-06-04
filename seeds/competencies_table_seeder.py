import random
from orator.seeds import Seeder
from orator.orm import Factory, Collection
from app.models.school import School
from app.models.user import User
from app.models.competence import Competence
from app.models.cource import Cource
from app.models.confirmation import Confirmation
from app.models.confirmation_file import ConfirmationFile
from datetime import datetime, timedelta

factory = Factory()


@factory.define(Competence)
def competence_factory(faker):
    return {
        'name': faker.sentence(nb_words=2),
        'description': faker.sentence(nb_words=10),
    }


@factory.define(Cource)
def cource_factory(faker):
    return {
        'name': faker.sentence(nb_words=4),
        'description': faker.sentence(nb_words=20),
        'start': faker.date_between(start_date='-180d', end_date='-30d')
    }


@factory.define(Confirmation)
def confirmation_factory(faker):
    return {
        'user_id': 1,
        'competence_id': 1,
        'status': random.choices(['processing', 'approved', 'declined'], [1, 1, 1], k=1),
    }


@factory.define(ConfirmationFile)
def confirmation_files_factory(faker):
    return {
        'file_url': 'https://cataas.com/cat?width={width}'.format(width=random.randint(20, 40)*10),
        'confirmation_id': 1,
    }


class CompetenciesTableSeeder(Seeder):

    factory = factory

    def run(self):
        """
        Run the database seeds.
        """
        competencies = self.factory(Competence, 10).create()
        cources = self.factory(Cource, 30).create()
        users = User.all()

        for cource in cources:
            comps = Collection()
            for x in range(random.randint(1, 4)):
                comps.push(random.choice(competencies))
            cource.competences().save_many(comps)

        for user in users:
            com_for_user = random.sample(
                list(competencies), random.randint(0, competencies.count()))
            user.competences().save_many(com_for_user)

        confirmations = Confirmation.all()
        for confirmation in confirmations:
            confirmation.status = random.choices(
                ['processing', 'approved', 'declined'], [1, 4, 1], k=1)[0]
            conf_file = Collection()
            for x in range(random.randint(1, 3)):
                conf_file.push(self.factory(ConfirmationFile).create())
            confirmation.confirmation_files().save_many(conf_file)
            confirmation.save()
