from app import db
from datetime import datetime

# Define a base model for other database document to inherit
class Base():

    __abstract__  = True

    date_created  = db.DateTimeField(default=datetime.utcnow)
    date_modified = db.DateTimeField(default=datetime.utcnow)

    # Pre-save behavior to update the date_modified field every time
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.date_modified = datetime.utcnow