from flask import Flask, url_for, render_template, jsonify, request, redirect, flash
from models import User, Category, ClassName, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)



@app.route('/login', methods=['GET', 'POST'])
def login():





@app.route('/')
@app.route('/home')
def home():
    # return 'the home page'
    return render_template('home.html')


@app.route('/categories')
def category_list():
    # return 'a list of all categories to choose from as well as latest items added'
    categories = session.query(Category).all()
    classes = session.query(ClassName).order_by('-id')[:5]
    if 'username' not in login_session:
        return render_template('home.html')
    else:
        return render_template('categories.html', categories=categories, classes=classes)


@app.route('/categories/<category_id>')
def class_list(category_id):
    # return 'list of all the classes in the catalog category'
    category = session.query(Category).filter_by(id=category_id).one()
    classes = session.query(ClassName).filter_by(category_id=category_id).all()
    return render_template('classes.html',  category=category, classes=classes)


@app.route('/categories/<category_id>/new', methods=['GET', 'POST'])
def add_class(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        new_class = ClassName(class_name=request.form['class_name'], category_id=category_id,
                              description=request.form['description'], user_id=login_session['user_id'])
        session.add(new_class)
        flash('Class was succesfully added', 'success')
        session.commit()
        return redirect(url_for('class_list', category_id=category_id))
    # return 'list of all the classes in the catalog category'
    else:
        return render_template('addclass.html',  category=category)


@app.route('/categories/<category_id>/<int:class_id>/edit', methods=['GET', 'POST'])
def edit_class(category_id, class_id):
    edited_class = session.query(ClassName).filter_by(id=class_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    classes = session.query(ClassName).filter_by(category_id=category_id).all()
    if request.method == 'POST':
        if request.form['class_name']:
            edited_class.class_name = request.form['class_name']
        if request.form['description']:
            edited_class.description = request.form['description']
        session.add(edited_class)
        session.commit()
        return redirect(url_for('class_list', category_id=category_id))
    # return 'list of all the classes in the catalog category'
    else:
        return render_template('editclass.html',  category=category, classes=classes, edit=edited_class)


@app.route('/categories/<category_id>/<int:class_id>/delete', methods=['GET', 'POST'])
def delete_class(category_id, class_id):
    category = session.query(Category).filter_by(id=category_id).one()
    del_class = session.query(ClassName).filter_by(id=class_id).one()
    if request.method == 'POST':
        session.delete(del_class)
        session.commit()
        return redirect(url_for('class_list', category_id=category_id))
    else:
        return render_template('deleteclass.html',  category=category, item=del_class)


@app.route('/categories/<category_id>/<int:class_id>')
def class_description(category_id, class_id):

    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(ClassName).filter_by(id=class_id).one()
    return render_template('class_description.html', category=category, item=item)

# API endpoints for classes and categories
@app.route('/categories/JSON')
def category_listJOSN():
    # return 'a list of all categories to choose from'
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/categories/<int:category_id>/JSON')
def class_listJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    classes = session.query(ClassName).filter_by(category_id=category_id).all()
    return jsonify(Classes=[i.serialize for i in classes])


@app.route('/categories/classes/JSON')
def all_classJSON():
    classes=session.query(ClassName).all()
    return jsonify(Classes=[i.serialize for i in classes])


def create_user():
    new_user = User(name=login_session['username'], email=login_session["email"])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    user = session.query(User).filter_by(email=email).one()
    if user:
        return user.id
    else:
        return None


if __name__ == '__main__':
    app.secret_key = 'secretKey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

