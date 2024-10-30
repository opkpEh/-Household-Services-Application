from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .. import db
from ..models import User, Professional, Service


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.admin_dashboard'))

        flash('Invalid username or password')
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.flush()  # Get user.id without committing

        if role == 'professional':
            professional = Professional(
                user_id=user.id,
                service_type=request.form.get('service_type'),
                experience=request.form.get('experience'),
                description=request.form.get('description'),
                location_pincode=request.form.get('pincode')
            )
            db.session.add(professional)

        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('auth.login'))

    services = Service.query.all()
    return render_template('auth/register.html', services=services)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))