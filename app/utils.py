import os
from typing import List

import requests
from flask import current_app
from requests import HTTPError
from sqlalchemy.exc import IntegrityError

from app import logger
from app.extensions import db
from app.models.skill import Skill as SkillModel  # Model
from app.models.user import User as UserModel  # Model
from app.types import User  # Type hinting


def initialize_db_with_json_data():
    logger = current_app.logger

    # Drop all tables and create new ones
    db.drop_all()
    db.create_all()

    try:
        users = _get_users()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        exit(1)

    _add_users_to_db(users)


def _add_users_to_db(users: List[User]) -> None:
    '''
    Add users to database
    '''
    logger = current_app.logger
    for user in users:
        user_obj = UserModel(
            name=user['name'], company=user['company'], email=user['email'], phone=user['phone'])
        try:
            db.session.add(user_obj)
            db.session.commit()
        except IntegrityError:
            # If user already exists, log error and continue
            logger.error(
                f'User with email {user["email"]} already exists')
            db.session.rollback()
            continue

        for skill in user['skills']:
            skill_obj = SkillModel(
                name=skill['skill'], rating=skill['rating'], user_id=user_obj.id)
            db.session.add(skill_obj)
            db.session.commit()


def _get_users() -> List[User]:
    '''
    Get data from API and return as JSON
    Raises HTTPError if status code is not 200
    '''
    response = requests.get(os.environ.get('API_URL'))

    response.raise_for_status()

    return response.json()
