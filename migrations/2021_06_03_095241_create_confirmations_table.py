from orator.migrations import Migration


class CreateConfirmationsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('confirmations') as table:
            table.big_increments('id')
            table.timestamps()
            table.big_integer('user_id')
            table.foreign('user_id').references('id').on('users')
            table.big_integer('competence_id')
            table.foreign('competence_id').references('id').on('competencies')
            table.string('status').default('processing')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('confirmations')
