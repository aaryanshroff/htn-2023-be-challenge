from flask import jsonify, request

from app.blueprints.events import bp
from app.extensions import db
from app.models.event import Event
from app.models.user import User


@bp.put('/<int:id>')
def scan_event(id):
    '''Scan a user into an event'''
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return 'No user id provided', 400
    user = User.query.get_or_404(data['user_id'])

    event = Event.query.get_or_404(id)

    # Check if user is already in event
    if user in event.users:
        return 'User already scanned into event', 400

    event.users.append(user)
    db.session.commit()

    return jsonify(event.to_dict())
