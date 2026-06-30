from app.database import get_connection
from datetime import datetime, timedelta
import random


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
def create_login_code(user_id):
    """Generate a 6 digit code for this user, store it with a 10 minute expiry, return the code."""
    code = "{:06d}".format(random.randint(0, 999999))
    expires_at = datetime.now() + timedelta(minutes=10)

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO auth_codes (user_id, code, purpose, expires_at)
                VALUES (%s, %s, 'login', %s)
                """,
                (user_id, code, expires_at),
            )
        connection.commit()
        return code
    finally:
        connection.close()


def verify_login_code(user_id, code):
    """Return True if there is a valid, unused, unexpired login code matching, and mark it used."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM auth_codes
                WHERE user_id = %s
                  AND code = %s
                  AND purpose = 'login'
                  AND used = FALSE
                  AND expires_at > %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id, code, datetime.now()),
            )
            row = cursor.fetchone()
            if not row:
                return False

            cursor.execute(
                "UPDATE auth_codes SET used = TRUE WHERE id = %s",
                (row["id"],),
            )
        connection.commit()
        return True
    finally:
        connection.close()
def get_user_by_id(user_id):
    """Return the user with this id, or None."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
    finally:
        connection.close()