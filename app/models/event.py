from app.extensions import db

event_user = db.Table('event_user',
                      db.Column('event_id', db.Integer, db.ForeignKey(
                          'event.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'user.id'), primary_key=True)
                      )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Event {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'users': [user.to_dict() for user in self.users]
        }
