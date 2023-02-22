## Instructions
### Docker
```zsh
docker compose up
```
### venv
Prerequisites
```zsh
export FLASK_APP=app.py
export API_URL=<json_data_source>
```
Run server
```zsh
python3 -m venv .venv
source .venv/bin/activate
flask run --port=3000
```

## Frameworks and Languages
- Flask (REST API)
- Flask-Caching
- SQLite (Database)
- Flask-SQLAlchemy (ORM)
- Docker

## API
### All Users Endpoint
`GET localhost:3000/users/`

### User Information Endpoint
`GET localhost:3000/users/1`

### Updating User Data Endpoint
Submitting the following JSON:
```javascript
  {
    "phone": "+1 (555) 123 4567"
  }
```
to the given URL: `PUT localhost:3000/users/1` updates their phone number to +1 (555) 123 4567 and return the full user data with the new phone number. If a user has new skills, these skills are added to the database. Any existing skills have their ratings updated.

### All Skills Endpoint
`GET localhost:3000/skills` returns skills and corresponding number of users (frequency).

`GET localhost:3000/skills/?min_frequency=20&max_frequency=30` returns skills and corresponding frequencies for skills with at least 20 users and at most 30 users.

*Since users do not gain/lose skills very often, the data returned by the all skills endpoint is cached to avoid querying DB each time.*

### Scan Event Endpoint
Submitting the following JSON:
```javascript
    {
        "user_id": 2
    }
```
to the given URL: `PUT localhost:3000/events/1` updates the users for event with event_id 1 to include the user with user_id 2. The user info endpoint now returns event 1 as part of user 2's events.