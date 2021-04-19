from flask import Flask, url_for, render_template, flash, request, redirect, session, current_app
from shop import app, db, paystack
from shop.products.models import Addproduct
import simplejson as json

paystack_secret_key = 'sk_test_25a564e7f472ec8650770fb6d7d06fc2e7b57285'

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



@app.route('/addcart', methods=['POST'])
def AddCarts():
    try:
        
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()


       
        
        if product_id  and quantity and colors and request.method == "POST":
            DictItems = {product_id:{'name' : product.name, 'price' : product.price, 'discount' : product.discount , 'quantity' : quantity, 'color' : colors , 'stock': product.stock, 'image' : product.image_1, 'colors':product.colors}}
            json.dumps(DictItems)

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:

                session['Shoppingcart'] = DictItems
                return redirect (request.referrer)
    except Exception as e:
        print(e)

    finally:
        return redirect(request.referrer)

       
@app.route('/carts')
def Cart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('brand.home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        deliveryFee = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('cartsproduct/cart.html', grandtotal=grandtotal, deliveryFee=deliveryFee)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('brand.home'))

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')

        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash(f'Your cart has been updated', 'success')
                    return redirect(url_for('Cart'))
        except Exception as e:
            return redirect(url_for('Cart'))
            print(e)

@app.route('/deletecart/<int:id>', methods=['POST'])
def deletecart(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))


    if request.method == 'POST':
        try:
            
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    session['Shoppingcart'].pop(key, None)
                    return redirect(url_for('Cart'))
                    flash(f'Your product has been removed', 'Success')




        except Exception as e:
            print(e)
            return redirect(url_for('Cart'))

            


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('brand.home'))
    except Exception as e:
        
        print(e)