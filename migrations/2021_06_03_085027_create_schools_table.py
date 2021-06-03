from orator.migrations import Migration


class CreateSchoolsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('schools') as table:
            table.big_increments('id')
            table.timestamps()
            table.string('name').unique()
            table.string('address')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('schools')
