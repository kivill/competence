from orator.migrations import Migration


class CreateConfirmationFilesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('confirmation_files') as table:
            table.big_increments('id')
            table.timestamps()
            table.string('file_url')
            table.big_integer('confirmation_id')
            table.foreign('confirmation_id').references('id').on('confirmations')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('confirmation_files')
