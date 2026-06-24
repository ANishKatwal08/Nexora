from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from datetime import datetime


# ---------- User Model ----------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Nexora-specific fields
    role = db.Column(db.String(20), default='learner')   # 'learner', 'mentor', or 'both'
    full_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    skills = db.Column(db.String(300))                   # comma-separated for now
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


# ---------- Public Pages ----------
def home():
    return render_template('home.html')


def about():
    return render_template('about.html')


# ---------- Registration ----------
def register_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'learner')
        full_name = request.form.get('full_name', '').strip()

        # Basic validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('auth.register'))

        if role not in ('learner', 'mentor', 'both'):
            role = 'learner'

        # Uniqueness checks
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(
            username=username,
            email=email,
            role=role,
            full_name=full_name
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ---------- Login ----------
def login_user():
    # If already logged in, send to dashboard
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('auth.dashboard'))

        flash('Invalid email or password.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


# ---------- Logout ----------
def logout_user():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


# ---------- Dashboard ----------
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # Show different dashboard based on role
    if user.role == 'mentor':
        return render_template('dashboard.html', user=user, view='mentor')
    elif user.role == 'both':
        return render_template('dashboard.html', user=user, view='both')
    else:
        return render_template('dashboard.html', user=user, view='learner')


# ---------- Profile ----------
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.full_name = request.form.get('full_name', '').strip()
        user.bio = request.form.get('bio', '').strip()
        user.skills = request.form.get('skills', '').strip()

        new_role = request.form.get('role')
        if new_role in ('learner', 'mentor', 'both'):
            user.role = new_role
            session['role'] = new_role

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('profile.html', user=user)