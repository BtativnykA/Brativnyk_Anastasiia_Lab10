"""DB-API demonstration using pure sqlite3."""

import sqlite3


def find_students_by_group_dbapi(database_path: str, group_name: str) -> list[tuple]:
    """Parameterized query (WHERE groups.name = ?) for SQL injection protection."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT students.first_name, students.last_name, students.average_grade
            FROM students
            JOIN groups ON students.group_id = groups.id
            WHERE groups.name = ?
            """,
            (group_name,),
        )
        return cursor.fetchall()
