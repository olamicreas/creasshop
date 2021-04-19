from flask import Flask, session, redirect, current_app, url_for, render_template, Blueprint, request, flash
from shop import app, db, photos, bcrypt, search, fa
from .forms import Addproducts
from shop.products.models import Brand, Category, Addproduct
import os, secrets

product_blueprint=Blueprint(
   'brand',
    __name__,
    template_folder='templates'
)




@product_blueprint.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=8)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.all()
    
    return render_template('iindex.html', products=products, brands=brands, categories=categories)

@product_blueprint.route('/result')
def result():
    searchword = request.args.get("q")
    products = Addproduct.query.msearch(searchword, fields=['name', 'description'], limit=3)
    return render_template('result.html', products=products)

@product_blueprint.route('/single_page/<int:id>')
def single_page(id):
    product = Addproduct.query.get(id)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('single_page.html', product=product, categories=categories, brands=brands)

@product_blueprint.route('/get_brand/<int:id>')
def get_brand(id):
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=4)
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('iindex.html', brand=brand, categories=categories, brands=brands, products=products)

@product_blueprint.route('/get_category/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=4)
    cats = Addproduct.query.filter_by(category_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('iindex.html', cats=cats, categories=categories, brands=brands, products=products)

@product_blueprint.route('/addbrand', methods=['POST', 'GET'])
def addbrand(): 
    if request.method == 'POST':

        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The brand {getbrand} was added to your database', 'success')
        return redirect(url_for('brand.addbrand'))
    return render_template('addbrand.html', brands='brands')


@product_blueprint.route('/addcat', methods=['POST', 'GET'])
def addcat():
    if request.method == 'POST':

        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        db.session.commit()
        flash(f'The category {getcat} was added to your database', 'success')
        return redirect(url_for('brand.addcat'))
    return render_template('addbrand.html')







@product_blueprint.route('/addproduct', methods=["POST", "GET"])
def addproduct():
    categories = Category.query.all()
    brands = Brand.query.all()
    form = Addproducts(request.form)

    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category = request.form.get('category')




        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        

        addprod = Addproduct(name=name, price=price, discount=discount, stock=stock, description=description, colors=colors, brand_id=brand, category_id=category,  image_1=image_1, image_2=image_2, image_3=image_3)

        db.session.add(addprod)
        flash(f'Your product {name} has been addded to database', 'success')
        db.session.commit()

        return redirect(url_for('users.admin'))
   


    return render_template('addproduct.html', form=form, categories=categories, brands=brands)


@product_blueprint.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')

    form = Addproducts(request.form)



    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.description = form.description.data
        product.colors = form.colors.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'),  name=secrets.token_hex(10) + ".")

            except:
                photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")


            except:
                photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")


        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")


            except:
                photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

    
        db.session.commit()
        flash(f'You have updated your product', 'success')
        return redirect(url_for('users.admin'))


    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data = product.description
    form.colors.data = product.colors










    return render_template('updateproduct.html', form=form,brands=brands, categories=categories, product=product)


@product_blueprint.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    updatebrand = Brand.query.get(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect('users.brands')
    return render_template('updatebrand.html', updatebrand=updatebrand)



@product_blueprint.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    updatecat = Category.query.get(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat = category
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect('users.category')
    return render_template('updatebrand.html', updatecat=updatecat)




@product_blueprint.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        return redirect(url_for('users.admin'))
        flash(f'Your brand has been deleted', 'success')

    flash(f'The brand {brand.name} cannot be deletd', 'danger')
    return redirect(url_for('users.admin'))


@product_blueprint.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    cat = Category.query.get(id)
    if request.method == 'POST':
        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for('users.admin'))
        flash(f'Your brand has been deleted', 'success')

    flash(f'The brand {cat.name} cannot be deletd', 'danger')
    return redirect(url_for('users.admin'))

@product_blueprint.route('/deleteproduct/<int:id>', methods=['POST', 'GET'])
def deleteproduct(id):
    product = Addproduct.query.get(id)
    if request.method == 'POST':
        
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product_image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product_image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product_image_3))
                

        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Your product {product.name} has been deleted', 'success')
        return redirect(url_for('users.admin'))
    flash(f'This product{product.name} can not be deleted', 'danger')
    return redirect(url_for('users.admin'))
