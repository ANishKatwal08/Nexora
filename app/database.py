import pymysql
from config import Config


def get_connection():
    """Open a new connection to the MySQL database."""
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
    )


def create_tables():
    """Create tables if they do not already exist."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120) NOT NULL,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    phone VARCHAR(20) UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'learner',
                    bio TEXT,
                    profession VARCHAR(120),
                    headline VARCHAR(150),
                    hourly_rate INT,
                    years_experience INT,
                    avatar_url VARCHAR(255),
                    rating DECIMAL(2,1) DEFAULT 0.0,
                    theme VARCHAR(10) DEFAULT 'light',
                    is_active BOOLEAN DEFAULT TRUE,
                    email_verified BOOLEAN DEFAULT FALSE,
                    failed_attempts INT DEFAULT 0,
                    lockout_until DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    code VARCHAR(10) NOT NULL,
                    purpose VARCHAR(20) NOT NULL DEFAULT 'login',
                    expires_at DATETIME NOT NULL,
                    used BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(80) UNIQUE NOT NULL,
                    category VARCHAR(60),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mentor_skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    mentor_id INT NOT NULL,
                    skill_id INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (mentor_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_mentor_skill (mentor_id, skill_id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS session_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    learner_id INT NOT NULL,
                    mentor_id INT NOT NULL,
                    skill_id INT,
                    note TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    payment_status VARCHAR(20) DEFAULT 'unpaid',
                    scheduled_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (mentor_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    request_id INT NOT NULL,
                    learner_id INT NOT NULL,
                    mentor_id INT NOT NULL,
                    rating INT NOT NULL,
                    comment TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (request_id) REFERENCES session_requests(id) ON DELETE CASCADE,
                    FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (mentor_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_request_feedback (request_id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sender_id INT NOT NULL,
                    recipient_id INT NOT NULL,
                    body TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
        connection.commit()
    finally:
        connection.close()


def seed_skills():
    """Add a starter set of skills if the table is empty."""
    starter = [
        ("Python", "Programming & Tech"),
        ("JavaScript", "Programming & Tech"),
        ("Web Development", "Programming & Tech"),
        ("Data Science", "Data & AI"),
        ("Machine Learning", "Data & AI"),
        ("UI Design", "Design & Creative"),
        ("Graphic Design", "Design & Creative"),
        ("Public Speaking", "Business & Marketing"),
        ("Digital Marketing", "Business & Marketing"),
        ("Spanish", "Languages"),
        ("English", "Languages"),
        ("Music Production", "Music & Audio"),
    ]
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS count FROM skills")
            if cursor.fetchone()["count"] == 0:
                cursor.executemany(
                    "INSERT INTO skills (name, category) VALUES (%s, %s)",
                    starter,
                )
        connection.commit()
    finally:
        connection.close()