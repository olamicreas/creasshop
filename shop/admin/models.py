from shop import db, bcrypt

class User(db.Model):
    __tablename__: 'user'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Text(db.Text)
    username = db.Column(db.Text,unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profile = db.Column(db.String(180), default='profile.jpg')


    def __init__(self, name, email, username, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')




    @classmethod
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username = username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user
        return False


    def __repr__(self):
        return '<User {}>'. format(self.name)



 