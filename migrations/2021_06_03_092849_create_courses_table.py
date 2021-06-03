from orator.migrations import Migration


class CreateCoursesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('courses') as table:
            table.big_increments('id')
            table.timestamps()
            table.string('name')
            table.string('description')
            table.timestamp('start')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('courses')
