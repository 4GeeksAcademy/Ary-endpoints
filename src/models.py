from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    first_name = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f'<User: {self.id} - {self.email}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                 "email": self.email,
                 "is active": self.is_active,
                 "first_name": self.first_name}

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f'<Characters: {self.id} - {self.name}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                 "name": self.name}

class FavoriteCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users")
    characters_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    characters = db.relationship("Characters")

    def __repr__(self):
        return f'<FavoriteCharacters: {self.id}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                 "user_id": self.user_id,
                 "characters_id": self.characters_id}

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f'<Planets: {self.id} - {self.name}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                 "name": self.name}

class FavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users")
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planets = db.relationship("Planets")

    def __repr__(self):
        return f'<FavoritePlanets: {self.id}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {"id": self.id,
                 "user_id": self.user_id,
                 " planets_id": self.planets_id}