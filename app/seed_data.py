from random import randint, choice as rc
from faker import Faker
from app import app, db
from models import Hero, Power, HeroPower

powers = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    powers_instances = []
    for power_info in powers:
        p = Power(**power_info)
        powers_instances.append(p)

    db.session.add_all(powers_instances)

    heroes = []
    for i in range(100):
        h = Hero(
            name=fake.name(),
            super_name=fake.unique.first_name(),
        )
        heroes.append(h)

    db.session.add_all(heroes)

    hero_powers = []
    for h in heroes:
        for i in range(randint(1, 3)):
            power = rc(powers_instances)
            strength = rc(["Strong", "Weak", "Average"])
            hero_power = HeroPower(hero=h, power=power, strength=strength)
            hero_powers.append(hero_power)

    db.session.add_all(hero_powers)

    db.session.commit()

print("🦸‍♀️ Heroes data seeding complete!")