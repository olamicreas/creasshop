from shop import db, bcrypt
from datetime import datetime

class Addproduct(db.Model):

    __searchable__ = ["name", "description"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='img.jpg.png')
    image_2 = db.Column(db.String(150), nullable=False, default='img.jpg.png')
    image_3 = db.Column(db.String(150), nullable=False, default='img.jpg.png')




    def __repr__(self):
        return '<Addproduct %r>' % self.name






    


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    def __repr__(self):
        return '<Brand %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return '<Category %r>' % self.name

