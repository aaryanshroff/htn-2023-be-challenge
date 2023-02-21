from flask import jsonify, render_template, request
from app.models.skill import Skill
from app.blueprints.users import bp
from app.extensions import db
from app.models.user import User


@bp.get('/')
def get_users():
    '''Get all users'''
    users = User.query.all()
    user_list = [user.to_dict() for user in users]

    return jsonify(user_list)


@bp.get('/<int:id>')
def get_user(id):
    '''Get a single user by id'''
    user = User.query.get_or_404(id)

    return jsonify(user.to_dict())


@bp.put('/<int:id>')
def update_user(id):
    '''Update a user's name, company, phone, and skills'''
    user = User.query.get_or_404(id)
    data = request.get_json()

    # Update non-relationship fields
    user.name = data.get('name', user.name)
    user.company = data.get('company', user.company)
    user.phone = data.get('phone', user.phone)

    # Update skills
    for skill in data.get('skills', []):
        user_skill = user.get_skill(skill['skill'])
        if user_skill:
            user_skill.rating = skill['rating']
        else:
            user.skills.append(
                Skill(name=skill['skill'], rating=skill['rating']))

    db.session.commit()

    return jsonify(user.to_dict())
