from flask import Blueprint, request, jsonify
from marvel_character.helpers import token_required
from marvel_character.models import db, Character , character_schema, characters_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'some': 'value'}

#Create Character Endpoint
@api.route('/characters', methods = ['POST'])
@token_required 
def create_character (our_user):

    fname = request.json['fname']
    lname = request.json['lname']
    superhero_name = request.json['superhero_name']
    description = request.json['description']
    weakness = request.json['weakness']
    normal_job = request.json['normal_job']
    team = request.json['team']
    gender = request.json['gender']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    character = Character (fname, lname, superhero_name, description, weakness, 
                           normal_job, team, gender, user_token)
    
    db.session.add(character )
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)

#Read 1 Single Character Endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character (our_user, id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character )
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

#Read all the characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(our_user):
    token = our_user.token
    characters = Character.query.filter_by(user_token = token).all()
    response = characters_schema.dump(characters)

    return jsonify(response)


#Update 1 Character by ID
@api.route('/characters/<id>', methods = ['PUT'])
@token_required
def update_character (our_user,id):
    character = Character.query.get(id)

    character.fname = request.json['fname']
    character.lname = request.json['lname']
    character.superhero_name = request.json['superhero_name']
    character.description = request.json['description']
    character.weakness = request.json['weakness']
    character.normal_job = request.json['normal_job']
    character.team = request.json['team']
    character.gender = request.json['gender']
    character.user_token = our_user.token

    db.session.commit()

    response = character_schema.dump(character )

    return jsonify(response)


#Delete 1 Character by ID
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character (our_user, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)




