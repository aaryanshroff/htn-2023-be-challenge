from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
