from app import app, db
from app.models.base import Base
from flask_login import UserMixin
from mongoengine import signals

# MongoEngine Document 
class User(UserMixin, db.Document, Base):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()
    name = db.StringField(max_length=30)
    role = db.IntField()

    def getRoleName(self):
        return app.config['ACCESS'][self.role]

# register pre save behavior - defined on Base.py
signals.pre_save.connect(User.pre_save, sender=User)