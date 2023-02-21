from app.extensions import db


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f'<Skill {self.id}: {self.name} ({self.rating})>'

    def to_dict(self):
        return {
            'skill': self.name,
            'rating': self.rating,
        }
