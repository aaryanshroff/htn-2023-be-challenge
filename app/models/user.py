from app.extensions import db
from app.models.event import event_user
from app.models.skill import Skill  # This is a class
from app.types import User as UserType  # This is a type hint, not a class


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    # One-to-many relationship
    skills = db.relationship('Skill', backref='user', lazy=True)
    # Many-to-many relationship
    events = db.relationship(
        'Event', secondary=event_user, lazy='subquery', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'

    def to_dict(self) -> UserType:
        return {
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'skills': [skill.to_dict() for skill in self.skills],
            'events': [event.id for event in self.events]
        }

    def get_skill(self, name: str) -> Skill:
        return next((skill for skill in self.skills if skill.name == name), None)
