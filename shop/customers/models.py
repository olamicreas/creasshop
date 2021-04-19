from shop import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin
import json


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)
class Register(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    contact = db.Column(db.String)
    address = db.Column(db.String)
    zipcode = db.Column(db.String)
    profile = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Register %r>' % self.name

class JsonEcodedDict(db.TypeDecorator):
    impl= db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return {}

        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}

        else:
            return json.loads(value)


class CustomerOrder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return '< CustomerOrder %r>' % self.invoice


db.create_all()