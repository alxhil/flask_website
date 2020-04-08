from flask import render_template, url_for, flash, redirect
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from app import app
from flask_login import login_user, current_user, logout_user, login_required
posts = [
	{
		'author': 'Alex Hill',
		'title' : 'Blog Post 1',
		'content': 'First post content',
		'date_posted': 'April 20th 2020'
	},
	{
		'author': 'Alex Hill',
		'title' : 'Blog Post 2',
		'content': 'First post content',
		'date_posted': 'April 20th 2020'
	}


]


@app.route("/")
@login_required
def home():
	try:
		return render_template('home.html',
							   posts=posts, title="home")
	except:
		return 'failed'
@app.route("/about")
@login_required
def about():
		return render_template('about.html', title="about")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('home'))

	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash(f'You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Login failed.', 'danger')
	return render_template('login.html', title ='Login', form=form)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')



