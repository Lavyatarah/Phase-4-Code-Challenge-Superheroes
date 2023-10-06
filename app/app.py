#!/usr/bin/env python3

from flask import Flask, make_response,request,jsonify
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes',methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()

    heroes_dict_list= [heroes.to_dict() for hero in heroes]

    response = make_response(
        jsonify(heroes_dict_list),
        200
    )

    return response

@app.route('/heroes/<int:id>',methods=['GET'])
def get_heroes_by_id(id):
    hero = Hero.query.filter_by(id=id).first()

    if hero:
        hero_dict = hero.to_dict()

        response = make_response(jsonify(hero_dict),200)

        return response
    else:
        response = make_response(jsonify(
            {
                "error": "Hero not found"
            }
        ))
        return response
    
@app.route('/powers' ,methods=['GET'])
def get_powers():
    powers = Power.query.all()

    powers_dict_list = [powers.to_dict() for power in powers]

    response =  make_response(jsonify(
        powers_dict_list
    ),200)

    return response

@app.route('/powers/<int:id>' ,methods=['GET','PATCH'])
def get_powers_by_id(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        error_response = make_response(jsonify({"error": "Power not found"}),404)
        
        return error_response
    
    
    if request.method == 'GET':
        power_dict = power.to_dict()
        response = make_response(jsonify(power_dict),200)
        return  response
       
    
    elif request.method == 'PATCH':
        data = request.get_json()

        for attr in data:
            setattr(power,attr,data[attr])

        try:
            db.session.add(power)
            db.session.commit()

            response_dict = power.to_dict()

            response = make_response(jsonify(
            response_dict
             ),200)

            return response
        except Exception as e:
            db.session.rollback()
            validation_fail_response = make_response(jsonify({"errors": ["validation errors"]}),400)
            return validation_fail_response

@app.route('/hero_powers',methods=['POST'])
def post_hero_powers():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            strength = data.get('strength')
            power_id = data.get('power_id')
            hero_id = data.get('hero_id')

            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)

            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)
            db.session.commit()

            hero_with_powers = Hero.query.get(hero_id)

            response = make_response(jsonify(hero_with_powers.to_dict()),201)
            return response

        except Exception as e:
            validation_fail_response = make_response(jsonify({"errors": ["validation errors"]}),400)
            return validation_fail_response

        

        


if __name__ == '__main__':
    app.run(port=5555)