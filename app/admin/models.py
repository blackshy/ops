from wtforms import BooleanField

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    pwdhash = db.Column(db.String())
    admin = db.Column(db.Bollean())

    def __init__(self, username, password, admin = False):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.admin = admin

    def is_admin(self):
        return self.admin

