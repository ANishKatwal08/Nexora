Nexora

Nexora is a collaborative learning and mentorship platform. People sign up either to learn or to mentor, and from there they can share skills, schedule solo or group sessions, and keep their learning resources in one place.

This project is still in active development, so some of the features below are being built out as I go.

What it does


Sign up and log in as a learner, mentor, or admin
Secure authentication with password hashing, email-based two-factor login, and password reset
Mentors can create, edit, and manage their sessions
Learners can browse, book, and keep track of their sessions
Leave feedback and view mentor ratings
Attach learning resources to sessions
Search and filter sessions by skill, rating, and more
A dashboard tailored to each role
Dark and light mode


Tech stack

LayerTechnologyBackendFlask (Python)DatabaseMySQLTemplatingJinja2FrontendHTML, CSS, JavaScriptTestingpytest

Project structure

nexora/
├── run.py              Entry point
├── config.py           Configuration (loads from .env)
├── requirements.txt    Python dependencies
├── schema.sql          MySQL database schema
└── app/
    ├── __init__.py     App factory
    ├── database.py     Database connection and table setup
    ├── auth.py         Access-control decorators
    ├── routes/         URL to controller mapping
    ├── controllers/    Application logic
    ├── repository/     Database queries
    ├── static/         CSS, JS, images
    └── templates/      Jinja2 templates

Getting started

You will need Python 3.8 or newer, MySQL Server with MySQL Workbench, and Git.

bash# Clone the repository
git clone https://github.com/ANishKatwal08/nexora.git
cd nexora

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Set up the database:
# create a database in MySQL Workbench, then run schema.sql
# (detailed steps to follow)

# Set up environment variables:
# copy .env.example to .env and fill in your own values

# Run the app
python run.py

Once it is running, the app is available at http://127.0.0.1:5000.

Detailed database and environment setup instructions will be added as the project settles.

Running tests

pytest

Test details will be added once the test suite is in place.

Author

Anish Katwal

License

This project was created for educational purposes.