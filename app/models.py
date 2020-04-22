from app import db

class Event(db.Model):
    __tablename__ = 'event'
    _id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    author = db.Column(db.String)
    title = db.Column(db.String)
    text = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True