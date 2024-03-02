"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets, FavoriteCharacters, FavoritePlanets

# Instancias Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
#Configuración de la DB
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {"message": "Hello, this is your GET /user response "}
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def handle_user():
    response_body= {}
    results = []
    users = db.session.execute(db.select(Users)).scalars()
    if users:
            for row in users:
                data = row.serialize()
                results.append(data)
            response_body["results"] = results
            response_body["message"] = "characters list: "
            return response_body, 200
    response_body["message"] = "No hay characters"
    return response_body, 400

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_users_favorites(user_id):
    response_body= {}
    results = []
    if request.method=='GET':
        #Lçogica para consultar la DB y devolver todos los usuarios 
        users = db.session.execute(db.select(Users, FavoriteCharacters, FavoritePlanets)
                            .join(FavoriteCharacters, Users.id==FavoriteCharacters.user_id, isouter=True)
                            .join(FavoritePlanets,   Users.id==FavoritePlanets.user_id,isouter=True)
                            .where(Users.id==user_id))
        #response_body['results']=[row.serialize() for row in users]
        #response_body[ "message"] = 'Metodo Get de users'
        if users:
            for row in users:
                user, favoriteCharacter, favorite_Planet = row 
                data = user.serialize()
                if favoriteCharacter:
                    data["Characters"]= favoriteCharacter.serialize()
                if favorite_Planet:
                    data["Planets"]= favorite_Planet.serialize()
                results.append(data)
            response_body["results"] = results
            return response_body, 200



@app.route('/characters', methods=['GET'])
def handle_characters():
    response_body= {}
    results = []
    characters = db.session.execute(db.select(Characters)).scalars()
    if characters:
            for row in characters:
                data = row.serialize()
                results.append(data)
            response_body["results"] = results
            response_body["message"] = "characters list: "
            return response_body, 200
    response_body["message"] = "No hay characters"
    return response_body, 400

@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_character_id(character_id):
    response_body= {}
    #character = db.session.execute(db.select(Characters).where(Characters.id==character_id)).scalar()
    character = db.session.get(Characters,character_id)
    response_body["results"] = character.serialize()
    response_body["message"] = "Bien hecho"
    return response_body, 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    response_body= {}
    results = []
    planets = db.session.execute(db.select(Planets)).scalars()
    if planets:
            for row in planets:
                data = row.serialize()
                results.append(data)
            response_body["results"] = results
            response_body["message"] = "characters list: "
            return response_body, 200
    response_body["message"] = "No hay characters"
    return response_body, 400

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planet_id(planets_id):
    response_body= {}
    planet = db.session.execute(db.select(Planets).where(Planets.id==planets_id)).scalar()
    response_body["results"] = planet.serialize()
    response_body["message"] = "Bien hecho"
    return response_body, 200


@app.route('/favorites/<int:user_id>/planets', methods=['POST'])
def add_favorite_planets(user_id):
    response_body = {}
    data = request.json   
    # toma una instancia del modelo: FavoritePlanets 
    favorite = FavoritePlanets(user_id = user_id, planets_id = data["planet_id"])  
    response_body["message"]= "Responde el POST"
    db.session.add(favorite)
    db.session.commit()
    return response_body

@app.route('/favorites/<int:user_id>/characters', methods=['POST'])
def add_favorite_characters(user_id):
    response_body = {}
    data = request.json   
    # toma una instancia del modelo: FavoritePlanets 
    favorite = FavoriteCharacters(user_id = user_id, characters_id = data["character_id"])
    response_body["message"]= "Responde el POST"
    db.session.add(favorite)
    db.session.commit()
    return response_body

@app.route('/favorites/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_characters(user_id,character_id):
    response_body = {}  
    # toma una instancia del modelo: FavoritePlanets 
    favorite = FavoriteCharacters.query.filter_by(user_id=user_id, characters_id=character_id).first()
    response_body["message"]= "Responde el Delete" 
    response_body["result"]= favorite
    db.session.delete(favorite)
    db.session.commit()
    return response_body

@app.route('/favorites/<int:user_id>/planets/<int:planet_id>', methods=['GET','DELETE'])
def delete_favorite_planets(user_id,planet_id):
    response_body = {}  
    # toma una instancia del modelo: FavoritePlanets 
    favorite = FavoritePlanets.query.filter_by(user_id=user_id, planets_id=planet_id).first()
    if favorite:
        if request.method == 'DELETE':
            response_body["message"]= "Responde el Delete" 
            response_body["result"]= favorite.serialize()
            db.session.delete(favorite)
            db.session.commit()
            return response_body
        if request.method == 'GET':
            response_body["message"]="GET"
            response_body["result"] = favorite.serialize()
            return response_body
    else:
        response_body["message"] = "NONE"
        return response_body, 400

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
