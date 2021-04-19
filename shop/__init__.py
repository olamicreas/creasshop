from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_uploads import IMAGES, configure_uploads, patch_request_class, UploadSet
from flask_msearch import Search 
from flask_login import LoginManager
import secrets
import os
from paystackapi.paystack import Paystack

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
fa = FontAwesome(app)
bcrypt = Bcrypt(app)
paystack = Paystack(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://olamicreas:mujeeb@localhost/shop'
app.config['SQALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
Paystack_SECRET_KEY  = 'sk_test_25a564e7f472ec8650770fb6d7d06fc2e7b57285'
Paystack_PUBLIC_KEY = 'pk_test_314dccd680068de3e230b7714972b3637607fbfb'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


db = SQLAlchemy(app)
search = Search()
search.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerlogin'
login_manager.needs_refresh_messsage_category='danger'
login_manager.login_message=u'Please login first'

from shop.customers import views
from shop.carts import cart
from shop.admin.views import admin_blueprint
from shop.products.views import product_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')

app.register_blueprint(product_blueprint, url_prefix='/products')