from app.database import get_connection


def create_group_session(mentor_id, title, description, skill_id, capacity, scheduled_at):
    """Create a new group session hosted by a mentor."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO group_sessions
                    (mentor_id, title, description, skill_id, capacity, scheduled_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (mentor_id, title, description, skill_id, capacity, scheduled_at),
            )
        connection.commit()
    finally:
        connection.close()


def get_open_group_sessions():
    """Return all open group sessions with mentor name, skill, and how many have joined."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT gs.*, u.name AS mentor_name, s.name AS skill_name,
                       (SELECT COUNT(*) FROM group_participants gp
                        WHERE gp.group_session_id = gs.id) AS joined_count
                FROM group_sessions gs
                JOIN users u ON gs.mentor_id = u.id
                LEFT JOIN skills s ON gs.skill_id = s.id
                WHERE gs.status = 'open'
                ORDER BY gs.scheduled_at ASC, gs.created_at DESC
                """
            )
            return cursor.fetchall()
    finally:
        connection.close()


def get_group_sessions_for_mentor(mentor_id):
    """Return group sessions created by a mentor, with join counts."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT gs.*, s.name AS skill_name,
                       (SELECT COUNT(*) FROM group_participants gp
                        WHERE gp.group_session_id = gs.id) AS joined_count
                FROM group_sessions gs
                LEFT JOIN skills s ON gs.skill_id = s.id
                WHERE gs.mentor_id = %s
                ORDER BY gs.created_at DESC
                """,
                (mentor_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def get_group_session_by_id(session_id):
    """Return one group session with mentor and skill names and join count."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT gs.*, u.name AS mentor_name, s.name AS skill_name,
                       (SELECT COUNT(*) FROM group_participants gp
                        WHERE gp.group_session_id = gs.id) AS joined_count
                FROM group_sessions gs
                JOIN users u ON gs.mentor_id = u.id
                LEFT JOIN skills s ON gs.skill_id = s.id
                WHERE gs.id = %s
                """,
                (session_id,),
            )
            return cursor.fetchone()
    finally:
        connection.close()


def get_participants(session_id):
    """Return the learners who joined a group session."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name
                FROM group_participants gp
                JOIN users u ON gp.learner_id = u.id
                WHERE gp.group_session_id = %s
                ORDER BY gp.joined_at ASC
                """,
                (session_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def has_joined(session_id, learner_id):
    """Check whether a learner has already joined a group session."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM group_participants WHERE group_session_id = %s AND learner_id = %s",
                (session_id, learner_id),
            )
            return cursor.fetchone() is not None
    finally:
        connection.close()


def join_group_session(session_id, learner_id):
    """Add a learner to a group session."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT IGNORE INTO group_participants (group_session_id, learner_id) VALUES (%s, %s)",
                (session_id, learner_id),
            )
        connection.commit()
    finally:
        connection.close()


def leave_group_session(session_id, learner_id):
    """Remove a learner from a group session."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM group_participants WHERE group_session_id = %s AND learner_id = %s",
                (session_id, learner_id),
            )
        connection.commit()
    finally:
        connection.close()


def delete_group_session(session_id, mentor_id):
    """Delete a group session, only if it belongs to the given mentor."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM group_sessions WHERE id = %s AND mentor_id = %s",
                (session_id, mentor_id),
            )
        connection.commit()
    finally:
        connection.close()