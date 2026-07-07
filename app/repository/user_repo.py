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


def update_user_profile(user_id, name, bio):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET name = %s, bio = %s WHERE id = %s",
                (name, bio, user_id),
            )
        connection.commit()
    finally:
        connection.close()


def update_user_avatar(user_id, filename):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET avatar_url = %s WHERE id = %s",
                (filename, user_id),
            )
        connection.commit()
    finally:
        connection.close()

def get_all_skills():
    """Return every skill in the master list, ordered by category then name."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM skills ORDER BY category, name")
            return cursor.fetchall()
    finally:
        connection.close()


def get_mentor_skills(mentor_id):
    """Return the skills a mentor teaches."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.id, s.name, s.category
                FROM mentor_skills ms
                JOIN skills s ON ms.skill_id = s.id
                WHERE ms.mentor_id = %s
                ORDER BY s.name
                """,
                (mentor_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def add_mentor_skill(mentor_id, skill_id):
    """Link a skill to a mentor. Ignores duplicates."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT IGNORE INTO mentor_skills (mentor_id, skill_id)
                VALUES (%s, %s)
                """,
                (mentor_id, skill_id),
            )
        connection.commit()
    finally:
        connection.close()


def remove_mentor_skill(mentor_id, skill_id):
    """Unlink a skill from a mentor."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM mentor_skills WHERE mentor_id = %s AND skill_id = %s",
                (mentor_id, skill_id),
            )
        connection.commit()
    finally:
        connection.close()


def update_profession(user_id, profession):
    """Set a mentor's profession title."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET profession = %s WHERE id = %s",
                (profession, user_id),
            )
        connection.commit()
    finally:
        connection.close()

def find_mentors_by_skill(skill_id):
    """Return all mentors who teach a given skill."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name, u.username, u.profession, u.bio, u.avatar_url
                FROM users u
                JOIN mentor_skills ms ON u.id = ms.mentor_id
                WHERE ms.skill_id = %s
                  AND u.role = 'mentor'
                  AND u.is_active = TRUE
                ORDER BY u.name
                """,
                (skill_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def get_all_mentors():
    """Return all active mentors, for browsing without a filter."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, username, profession, bio, avatar_url
                FROM users
                WHERE role = 'mentor' AND is_active = TRUE
                ORDER BY name
                """
            )
            return cursor.fetchall()
    finally:
        connection.close()

def get_all_mentors(sort="rating"):
    """Return all active mentors, sorted by rating or name."""
    order = "rating DESC, name ASC" if sort == "rating" else "name ASC"
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT id, name, username, profession, bio, avatar_url, rating
                FROM users
                WHERE role = 'mentor' AND is_active = TRUE
                ORDER BY {order}
                """
            )
            return cursor.fetchall()
    finally:
        connection.close()
def create_session_request(learner_id, mentor_id, skill_id, note):
    """Create a new session request from a learner to a mentor."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO session_requests (learner_id, mentor_id, skill_id, note)
                VALUES (%s, %s, %s, %s)
                """,
                (learner_id, mentor_id, skill_id, note),
            )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_requests_for_learner(learner_id):
    """Return all session requests made by a learner, with mentor and skill names."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT sr.*, u.name AS mentor_name, s.name AS skill_name
                FROM session_requests sr
                JOIN users u ON sr.mentor_id = u.id
                LEFT JOIN skills s ON sr.skill_id = s.id
                WHERE sr.learner_id = %s
                ORDER BY sr.created_at DESC
                """,
                (learner_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def get_requests_for_mentor(mentor_id):
    """Return all session requests sent to a mentor, with learner and skill names."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT sr.*, u.name AS learner_name, s.name AS skill_name
                FROM session_requests sr
                JOIN users u ON sr.learner_id = u.id
                LEFT JOIN skills s ON sr.skill_id = s.id
                WHERE sr.mentor_id = %s
                ORDER BY sr.created_at DESC
                """,
                (mentor_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()


def get_request_by_id(request_id):
    """Return a single session request."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM session_requests WHERE id = %s", (request_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def update_request_status(request_id, status, scheduled_at=None):
    """Update a request's status and optionally its scheduled time."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE session_requests SET status = %s, scheduled_at = %s WHERE id = %s",
                (status, scheduled_at, request_id),
            )
        connection.commit()
    finally:
        connection.close()

def get_password_hash(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT password_hash FROM users WHERE id = %s",
                (user_id,),
            )
            row = cursor.fetchone()
            return row["password_hash"] if row else None
    finally:
        connection.close()


def update_password(user_id, new_hash):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_hash, user_id),
            )
        connection.commit()
    finally:
        connection.close()


def delete_user(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
    finally:
        connection.close()

def create_feedback(request_id, learner_id, mentor_id, rating, comment):
    """Save a review for a completed session, then refresh the mentor's average rating."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO feedback (request_id, learner_id, mentor_id, rating, comment)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (request_id, learner_id, mentor_id, rating, comment),
            )
            # Recompute the mentor's average rating from all their feedback
            cursor.execute(
                "SELECT AVG(rating) AS avg_rating FROM feedback WHERE mentor_id = %s",
                (mentor_id,),
            )
            avg = cursor.fetchone()["avg_rating"]
            cursor.execute(
                "UPDATE users SET rating = %s WHERE id = %s",
                (round(avg, 1), mentor_id),
            )
        connection.commit()
    finally:
        connection.close()


def get_feedback_for_request(request_id):
    """Return the review for a session, or None."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM feedback WHERE request_id = %s", (request_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def get_feedback_for_mentor(mentor_id):
    """Return all reviews for a mentor, with the learner name."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT f.*, u.name AS learner_name
                FROM feedback f
                JOIN users u ON f.learner_id = u.id
                WHERE f.mentor_id = %s
                ORDER BY f.created_at DESC
                """,
                (mentor_id,),
            )
            return cursor.fetchall()
    finally:
        connection.close()

def update_mentor_details(user_id, profession, headline, hourly_rate, years_experience):
    """Update a mentor's profile detail fields."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET profession = %s, headline = %s, hourly_rate = %s, years_experience = %s
                WHERE id = %s
                """,
                (profession, headline, hourly_rate, years_experience, user_id),
            )
        connection.commit()
    finally:
        connection.close()