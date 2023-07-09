from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_character.forms import CharacterForm
from marvel_character.models import Character, db 

site = Blueprint('site', __name__, template_folder='site_template')

@site.route('/')
def home():
    print('look at this cool project. Would you just look at it')
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    marvelform = CharacterForm()

    try:
        if request.method == 'POST' and marvelform.validate_on_submit():
            fname = marvelform.fname.data
            lname = marvelform.lname.data
            superhero_name = marvelform.superhero_name.data
            description = marvelform.description.data
            weakness = marvelform.weakness.data
            normal_job = marvelform.normal_job.data
            team = marvelform.team.data
            gender = marvelform.gender.data
            user_token = current_user.token 

            character = Character(fname, lname, superhero_name, description, weakness, normal_job, team, gender,  user_token)
            
            db.session.add(character)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Character not created, please check your form and try again.')
    
    user_token = current_user.token 
    characters = Character.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=marvelform, characters=characters)