from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    super_name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Hero(id={self.id}, name="{self.name}")'

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    def __repr__(self):
        return f'HeroPower(id={self.id}, hero_id={self.hero_id}, power_id={self.power_id})'
    
    @validates('strength')
    def validate_strength(self,key,strength):
        strengths = ["Strong","Weak","Average"]
        if strength not in strengths:
            raise ValueError('Use valid strength')
        return strength

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    description = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

    def __repr__(self):
        return f'Power(id={self.id}, name="{self.name}")'
    
    @validates('description')
    def validate_description(self,key,string):
        if not string:
            raise ValueError('Description required')
        if len(string) < 20:
            raise ValueError('Description should atleast be 20 characters long')












