from flask import Flask, make_response, render_template, session, request, url_for, Blueprint, flash, redirect
from shop import db, bcrypt
from shop.admin.forms import RegisterForm, LoginForm
from shop.admin.models import User
from shop.products.models import Addproduct, Brand, Category 


import os
from sqlalchemy.exc import IntegrityError 
admin_blueprint=Blueprint(
   'users',
    __name__,
    template_folder='templates'
)




@admin_blueprint.route('/admin')

def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('users.login')) 

    products = Addproduct.query.all()
    return render_template('index.html', products=products)
    

@admin_blueprint.route('/register', methods=['GET', 'POST'])
def register():
  

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
         

        new_user = User(form.name.data, form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Welcome {form.email.data} You have succesfully registered', 'success')
            
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Registration')


@admin_blueprint.route('/brand')
def brand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('users.login'))
    brands = Brand.query.order_by(Brand.id.description)
    return render_template('brand.html', brands=brands)




@admin_blueprint.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('users.login'))
    categories = Category.query.order_by(Category.id.description)
    return render_template('brand.html', categories=categories)










@admin_blueprint.route('/login', methods=['POST', 'GET'])
def login():
 
  
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(form.email.data, form.password.data)
            if user:

                session['email'] = form.email.data
                flash(f'Welcome {form.email.data}', 'success')
                return redirect(url_for('users.admin'))
        else:
            flash('Wrong password', 'danger')
        
    return render_template('login.html', form=form, title='Login page')


@admin_blueprint.route('/logout')
def logout():
  session.pop('email', None)
  flash('You have been signed out.')
  return redirect(url_for('users.login'))
