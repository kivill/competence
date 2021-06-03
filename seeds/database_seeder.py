from orator.seeds import Seeder
from seeds.school_table_seeder import SchoolTableSeeder
from seeds.competencies_table_seeder import CompetenciesTableSeeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(SchoolTableSeeder)
        self.call(CompetenciesTableSeeder)
