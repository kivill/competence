from orator.migrations import Migration


class CreateCoursesCompetenciesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('courses_competencies') as table:
            table.big_integer('course_id')
            table.foreign('course_id').references('id').on('courses')
            table.big_integer('competence_id')
            table.foreign('competence_id').references('id').on('competencies')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('courses_competencies')
