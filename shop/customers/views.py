from flask import Flask, render_template, url_for, request, redirect, flash, current_app, session
from shop import app, db, search, bcrypt, login_manager, paystack
from flask_login import login_required, current_user, logout_user, login_user
from shop.customers.models import Register, CustomerOrder
from shop.products.models import Addproduct
from shop.customers.forms import CustomerRegistrationForm, LoginForm
from pypaystack import Transaction, Customer, Plan
import secrets
import os
import simplejson as json
from paystackapi.transaction import Transaction

Paystack_secret_key  = 'sk_test_25a564e7f472ec8650770fb6d7d06fc2e7b57285'
Paystack_public_key = 'pk_test_314dccd680068de3e230b7714972b3637607fbfb'

import random
import string
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    
        

    
    amount = request.form.get('amount')
    email  = request.form.get('user-email')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    invoice = request.form.get('invoice')
    
    

        

            
    customer = Customer(authorization_key="sk_test_25a564e7f472ec8650770fb6d7d06fc2e7b57285")
    client = customer.create(first_name='first_name', last_name='last_name', email='email')        
    init = Transaction.initialize(reference='invoice',
                                  amount='amount', email='email')
    json.dumps(init)

           

    charge = Transaction.charge(reference='invoice',
                                authorization_code='sk_test_25a564e7f472ec8650770fb6d7d06fc2e7b57285',
                                email='email',
                                amount='amount')
            


    return render_template('customer/checkout.html', charge=charge, amount=amount, email=email, orders=orders, init=init, client=client,first_name=first_name, last_name=last_name, invoice=invoice) 

    
       
   
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerRegistrationForm(request.form)
    

    if request.method=='POST':
        try:

            hash_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data, city=form.city.data, state=form.state.data, contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
            db.session.add(register)
            
            
            db.session.commit()
            flash(f'Welcome {form.name.data} Thank you for registering', 'success')
            return redirect(url_for('customer_login'))
        
        except Exception as e:
            flash(f'Username or email has  already been taken', 'danger')
            print(e)


    
    return render_template('customer/register.html', form=form)






@app.route('/login', methods=['GET', 'POST'])
def customerlogin():
    form = LoginForm()
    if request.method=='POST' and form.validate():
        user = Register.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"You are now logged in", 'success')
            next = request.args.get('next')
            return redirect(next or url_for('brand.home'))
    
        
        flash(f'Incorrect password or username, try again', 'danger')
    
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    flash(f'You are now logged out', 'success')
    return redirect (url_for('brand.home'))

@app.route('/getOrder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)

        try:
        
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart', None) 
            
            flash(f'Your order has been sent', 'success')
           
            
            return redirect(url_for('orders', customer_id=customer_id, invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while ordering', 'danger')
            return redirect(url_for('Cart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            deliveryFee = ('%.2f' % (.6 * float(subTotal)))
            grandTotal = ('%.2f' % (1.06 * float(subTotal)))
        
    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html', grandTotal=grandTotal, deliveryFee=deliveryFee, subTotal=subTotal, customer=customer, customer_id=customer_id, orders=orders)
