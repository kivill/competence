from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.big_increments('id')
            table.timestamps()
            table.big_integer('school_id')
            table.foreign('school_id').references('id').on('schools')
            table.string('full_name')
            table.string('email').unique()
            table.string('password')
            table.string('role').default('учитель')
            table.text('token').nullable()
            table.text('refresh_token').nullable()
            table.text('uuid').unique()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('users')
