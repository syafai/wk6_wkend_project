from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_character.forms import UserLoginForm
from marvel_character.models import User, db, check_password_hash 

from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    userform = UserLoginForm()

    try:
        if request.method == 'POST' and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data
            print(email, password)

            user = User(email, username, password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('auth.signin'))
        
        
    except:
        raise Exception('Invalid Form Data. Please Check your form')
    
    return render_template('signup.html', form=userform)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    userform = UserLoginForm()


    try:
        if request.method == "POST" and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data 
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in via: Email/Password', 'auth-success')
                return redirect(url_for('site.profile')) #Come back to here and redirect to profile 
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
            
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form=userform )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
