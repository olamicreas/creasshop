from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, DecimalField, IntegerField, TextAreaField, BooleanField, validators, StringField


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    discount = DecimalField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "Image only please")])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "Image only please")])
    image_3 = FileField('Image 3', validators=[FileAllowed(['[jpg', 'png', 'gif', 'jpeg'], "Image only please")])