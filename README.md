# Nexora

Nexora is a collaborative learning and mentorship platform. Learners find mentors across a wide range of skills, request one on one sessions, message their mentors, and leave reviews afterwards. Mentors manage their profile, respond to session requests, and build a rating from real feedback. An admin oversees the whole platform.

This project was built with Flask and MySQL using a clean layered structure, with a focus on security, role based access, and a polished user interface.

## Features

**Accounts and security**
- Registration and login with multiple identifiers (email, username, or phone)
- Two step verification: after the password, a six digit code is emailed and must be entered to finish signing in
- Passwords hashed with Werkzeug, never stored in plain text
- CSRF protection on every form
- Change password and delete account from settings

**Roles**

Nexora has three roles, each with its own dashboard and permissions.
- Learner: browse mentors, request sessions, message mentors, leave reviews
- Mentor: set up a mentor profile, manage skills, respond to requests, host sessions
- Admin: view platform statistics and manage users, including activating and deactivating accounts

**Mentorship**
- A searchable mentor marketplace with category and skill filters, name search, and sorting by rating
- Detailed mentor profiles with profession, headline, rate, experience, skills, and reviews
- A full session request flow: request, confirm with a time, decline, and mark completed
- Ratings and written reviews after completed sessions, which update a mentor's average rating

**Communication**
- Direct messaging between learners and mentors
- A notification system for new requests, responses, and messages

**Experience**
- A modern dashboard with light and dark themes
- A help centre with a frequently asked questions section and support contact

## Tech stack

- Backend: Python, Flask with blueprints
- Database: MySQL, accessed with raw pymysql and parameterized queries
- Frontend: HTML, CSS, and vanilla JavaScript with Jinja templates
- Email: Gmail SMTP for verification codes
- Structure: a layered design of routes, controllers, and a repository, with tables created on startup

## Project structure

```
Nexora/
    run.py
    config.py
    requirements.txt
    app/
        __init__.py
        database.py
        auth.py
        email_service.py
        controllers/
            authController.py
            dashboardController.py
            profileController.py
            browseController.py
            mentorController.py
            sessionController.py
            settingsController.py
            messageController.py
            helpController.py
            adminController.py
        routes/
        repository/
            user_repo.py
        templates/
            base.html
            dash_base.html
            home.html
            auth/
            dashboard/
            partials/
        static/
            css/
            js/
            img/
            uploads/
```

## Setup and installation

### Prerequisites
- Python 3.10 or newer
- MySQL Server and MySQL Workbench
- A Gmail account with an app password, for sending verification emails

### Steps

1. Clone the repository

```
git clone https://github.com/ANishKatwal08/Nexora.git
cd Nexora
```

2. Create and activate a virtual environment

On Windows:

```
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```
pip install -r requirements.txt
```

4. Create the database

In MySQL Workbench, create a database named nexora:

```
CREATE DATABASE nexora;
```

The application creates all the tables automatically when it first runs.

5. Set up the environment file

Create a file named .env in the project root with your own values:

```
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=nexora
MAIL_SENDER=your-gmail-address
MAIL_APP_PASSWORD=your-gmail-app-password
```

The .env file is kept out of version control and should never be shared.

6. Run the application

```
python run.py
```

Open a browser to http://127.0.0.1:5000

## Test accounts

To try the two main roles, register your own learner and mentor accounts. Because login uses email verification, use an email address you can actually receive mail at, so you can read the code.

The admin account is created by registering a normal account, then promoting it in the database:

```
UPDATE nexora.users SET role = 'admin' WHERE email = 'your-email@example.com';
```

Log out and back in for the change to take effect.

## Notes

- The mentor marketplace is populated with sample mentor accounts so the browsing, filtering, and search features can be demonstrated. These are clearly marked sample data.
- All session, message, and review data is created through normal use of the application.

## Author

Built by Anish Katwal as a collaborative learning platform project.