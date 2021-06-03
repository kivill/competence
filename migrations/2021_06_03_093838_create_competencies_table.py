from orator.migrations import Migration


class CreateCompetenciesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('competencies') as table:
            table.big_increments('id')
            table.timestamps()
            table.string('name')
            table.string('description')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('competencies')
