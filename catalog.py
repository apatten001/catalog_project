from flask import Flask, url_for, render_template, jsonify, request, redirect, flash
from models import Category, ClassName, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from flask import make_response

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import string
import random
import requests
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret_catalog.json', 'r').read())['web']['client_id']


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# login a google account holder
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameters'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret_catalog.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade authorization code'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']

    # see if user exist, if not create a user
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:' \
              ' 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# logout connected google account holder
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print(access_token)
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ', login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# return 'the home page'
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/categories')
def category_list():
    # return 'a list of all categories to choose from as well as latest items added'
    categories = session.query(Category).all()
    classes = session.query(ClassName).order_by('-id')[:5]
    return render_template('index.html', categories=categories, classes=classes)


# function to add a category to database
@app.route('/category/new', methods=['GET', 'POST'])
def add_category():
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    if request.method == 'POST':
        new_category = Category(category_name=request.form['category_name'], user_id=login_session['user_id'])
        session.add(new_category)
        flash('Category was successfully created', 'success')
        session.commit()
        return redirect(url_for('category_list'))
    else:
        return render_template('addcategory.html')


# return 'list of all the classes in the catalog category'
@app.route('/categories/<category_name>')
def class_list(category_name):
    category = session.query(Category).filter_by(category_name=category_name).one()
    classes = session.query(ClassName).filter_by(category_id=category.id).all()
    creator = get_user_info(category.user_id)
    if 'username' not in login_session:
        return render_template('public_classes.html', category=category, classes=classes, creator=creator)
    else:
        return render_template('classes.html',  category=category, classes=classes)


# function to add a class to database
@app.route('/categories/<category_name>/new', methods=['GET', 'POST'])
def add_class(category_name):
    category = session.query(Category).filter_by(category_name=category_name).one()
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    if request.method == 'POST':
        new_class = ClassName(class_name=request.form['class_name'], category_id=category.id,
                              description=request.form['description'], user_id=login_session['user_id'])
        session.add(new_class)
        flash('Class was succesfully added', 'success')
        session.commit()
        return redirect(url_for('class_list', category_name=category_name))
    # return 'list of all the classes in the catalog category'
    else:
        return render_template('addclass.html',  category=category)


# allows edit class functionality to logged in users
@app.route('/categories/<category_name>/<int:class_id>/edit', methods=['GET', 'POST'])
def edit_class(category_name, class_id):
    edited_class = session.query(ClassName).filter_by(id=class_id).one()
    category = session.query(Category).filter_by(category_name=category_name).one()
    classes = session.query(ClassName).filter_by(category_id=category.id).all()
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    if request.method == 'POST':
        if request.form['class_name']:
            edited_class.class_name = request.form['class_name']
        if request.form['description']:
            edited_class.description = request.form['description']
        session.add(edited_class)
        session.commit()
        return redirect(url_for('class_list', category_name=category_name))
    # return 'list of all the classes in the catalog category'
    else:
        return render_template('editclass.html',  category=category, classes=classes, edit=edited_class)


# allows delete class functionality to logged in users
@app.route('/categories/<category_name>/<int:class_id>/delete', methods=['GET', 'POST'])
def delete_class(category_name, class_id):
    category = session.query(Category).filter_by(category_name=category_name).one()
    del_class = session.query(ClassName).filter_by(id=class_id).one()
    if 'username' not in login_session:
        return redirect(url_for('show_login'))
    if request.method == 'POST':
        session.delete(del_class)
        session.commit()
        return redirect(url_for('class_list', category_name=category_name))
    else:
        return render_template('deleteclass.html',  category=category, item=del_class)


# displays the description of specified class
@app.route('/categories/<category_name>/<int:class_id>')
def class_description(category_name, class_id):

    category = session.query(Category).filter_by(category_name=category_name).one()
    item = session.query(ClassName).filter_by(id=class_id).one()
    creator = get_user_info(item.user_id)
    print(creator)
    if 'username' not in login_session:
        return render_template('publicclassdescription.html', category=category, item=item, creator=creator)
    return render_template('class_description.html', category=category, item=item, creator=creator)


# API endpoints for classes and categories
@app.route('/api/v1/categories/JSON')
def category_listJOSN():
    # return 'a list of all categories to choose from'
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/api/v1/categories/<int:category_id>/JSON')
def class_listJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    classes = session.query(ClassName).filter_by(category_id=category_id).all()
    return jsonify(Classes=[i.serialize for i in classes])


@app.route('/api/v1/categories/classes/JSON')
def all_classJSON():
    classes=session.query(ClassName).all()
    return jsonify(Classes=[i.serialize for i in classes])


# function that creates users
def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session["email"], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user.id
    else:
        return None


if __name__ == '__main__':
    app.secret_key = 'secretKey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

