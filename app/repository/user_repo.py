from app.database import get_connection


def create_user(name, username, email, phone, password_hash, role):
    """Insert a new user and return the new user id."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, username, email, phone, password_hash, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, username, email, phone, password_hash, role),
            )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_user_by_email(email):
    """Return the user with this email, or None."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    finally:
        connection.close()


def get_user_by_username(username):
    """Return the user with this username, or None."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
    finally:
        connection.close()
def get_user_by_identifier(identifier):
    """Return the user whose email, username, or phone matches, or None."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM users
                WHERE email = %s OR username = %s OR phone = %s
                """,
                (identifier, identifier, identifier),
            )
            return cursor.fetchone()
    finally:
        connection.close()