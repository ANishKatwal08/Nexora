from app.database import get_connection


def get_profile_by_user(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, profession, headline, bio,
                       skills, years_experience, hourly_rate
                FROM mentor_profiles
                WHERE user_id = %s
                """,
                (user_id,),
            )
            return cursor.fetchone()
    finally:
        connection.close()


def create_profile(user_id, profession, headline, bio, skills, years, rate):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO mentor_profiles
                    (user_id, profession, headline, bio, skills, years_experience, hourly_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, profession, headline, bio, skills, years, rate),
            )
        connection.commit()
    finally:
        connection.close()


def update_profile(user_id, profession, headline, bio, skills, years, rate):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE mentor_profiles
                SET profession = %s, headline = %s, bio = %s,
                    skills = %s, years_experience = %s, hourly_rate = %s
                WHERE user_id = %s
                """,
                (profession, headline, bio, skills, years, rate, user_id),
            )
        connection.commit()
    finally:
        connection.close()


def delete_profile(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM mentor_profiles WHERE user_id = %s",
                (user_id,),
            )
        connection.commit()
    finally:
        connection.close()