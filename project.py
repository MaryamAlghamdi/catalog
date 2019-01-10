from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, LearningCourses, cListItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///LcourseslcListwithusers.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# JSON APIs to view Learning Courses Information


@app.route('/Lcourses/<int:Lcourses_id>/lcList/JSON')
def LcoursescListJSON(Lcourses_id):
    Lcourses = session.query(LearningCourses).filter_by(id=Lcourses_id).one()
    items = session.query(cListItem).filter_by(
        Lcourses_id=Lcourses_id).all()
    return jsonify(cListItems=[i.serialize for i in items])


@app.route('/Lcourses/<int:Lcourses_id>/lcList/<int:lcList_id>/JSON')
def lcListItemJSON(Lcourses_id, lcList_id):
    cList_Item = session.query(cListItem).filter_by(id=lcList_id).one()
    return jsonify(cList_Item=cList_Item.serialize)


@app.route('/Lcourses/JSON')
def LcoursessJSON():
    Lcoursess = session.query(LearningCourses).all()
    return jsonify(Lcoursess=[r.serialize for r in Lcoursess])


# Show all courses
@app.route('/')
@app.route('/Lcourses/')
def showLearningCourses():
    Lcoursess = session.query(LearningCourses).order_by(asc(LearningCourses.name))
    if 'username' not in login_session:
        return render_template('publicLcoursess.html', Lcoursess=Lcoursess)
    else:
        return render_template('Lcoursess.html', Lcoursess=Lcoursess)

# Create a new Course


@app.route('/Lcourses/new/', methods=['GET', 'POST'])
def newLearningCourses():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newLearningCourses = LearningCourses(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newLearningCourses)
        flash('New LearningCourses %s Successfully Created' % newLearningCourses.name)
        session.commit()
        return redirect(url_for('showLearningCourses'))
    else:
        return render_template('newLcourses.html')

# Edit a Course


@app.route('/Lcourses/<int:Lcourses_id>/edit/', methods=['GET', 'POST'])
def editLearningCourses(Lcourses_id):
    editedLearningCourses = session.query(
        LearningCourses).filter_by(id=Lcourses_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedLearningCourses.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this Lcourses. Please create your own Lcourses in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedLearningCourses.name = request.form['name']
            flash('LearningCourses Successfully Edited %s' % editedLearningCourses.name)
            return redirect(url_for('showLearningCourses'))
    else:
        return render_template('editLcourses.html', Lcourses=editedLearningCourses)


# Delete Course


@app.route('/Lcourses/<int:Lcourses_id>/delete/', methods=['GET', 'POST'])
def deleteLearningCourses(Lcourses_id):
    LcoursesToDelete = session.query(
        LearningCourses).filter_by(id=Lcourses_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if LcoursesToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this Lcourses. Please create your own Lcourses in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(LcoursesToDelete)
        flash('%s Successfully Deleted' % LcoursesToDelete.name)
        session.commit()
        return redirect(url_for('showLearningCourses', Lcourses_id=Lcourses_id))
    else:
        return render_template('deleteLcourses.html', Lcourses=LcoursesToDelete)

# Show the course Items


@app.route('/Lcourses/<int:Lcourses_id>/')
@app.route('/Lcourses/<int:Lcourses_id>/lcList/')
def showcList(Lcourses_id):
    Lcourses = session.query(LearningCourses).filter_by(id=Lcourses_id).one()
    creator = getUserInfo(Lcourses.user_id)
    items = session.query(cListItem).filter_by(
        Lcourses_id=Lcourses_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publiclcList.html', items=items, Lcourses=Lcourses, creator=creator)
    else:
        return render_template('lcList.html', items=items, Lcourses=Lcourses, creator=creator)


# Create a new Course item


@app.route('/Lcourses/<int:Lcourses_id>/lcList/new/', methods=['GET', 'POST'])
def newcListItem(Lcourses_id):
    if 'username' not in login_session:
        return redirect('/login')
    Lcourses = session.query(LearningCourses).filter_by(id=Lcourses_id).one()
    if request.method == 'POST':
        newItem = cListItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], Lcourses_id=Lcourses_id, user_id=Lcourses.user_id)
        session.add(newItem)
        session.commit()
        flash('New cList %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showcList', Lcourses_id=Lcourses_id))
    else:
        return render_template('newlcListitem.html', Lcourses_id=Lcourses_id)

# Edit Course item


@app.route('/Lcourses/<int:Lcourses_id>/lcList/<int:lcList_id>/edit', methods=['GET', 'POST'])
def editcListItem(Lcourses_id, lcList_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(cListItem).filter_by(id=lcList_id).one()
    Lcourses = session.query(LearningCourses).filter_by(id=Lcourses_id).one()
    if login_session['user_id'] != Lcourses.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit lcList items to this Lcourses. Please create your own Lcourses in order to edit items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('cList Item Successfully Edited')
        return redirect(url_for('showcList', Lcourses_id=Lcourses_id))
    else:
        return render_template('editlcListitem.html', Lcourses_id=Lcourses_id, lcList_id=lcList_id, item=editedItem)


# Delete Course item


@app.route('/Lcourses/<int:Lcourses_id>/lcList/<int:lcList_id>/delete', methods=['GET', 'POST'])
def deletecListItem(Lcourses_id, lcList_id):
    if 'username' not in login_session:
        return redirect('/login')
    Lcourses = session.query(LearningCourses).filter_by(id=Lcourses_id).one()
    itemToDelete = session.query(cListItem).filter_by(id=lcList_id).one()
    if login_session['user_id'] != Lcourses.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete lcList items to this Lcourses. Please create your own Lcourses in order to delete items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('cList Item Successfully Deleted')
        return redirect(url_for('showcList', Lcourses_id=Lcourses_id))
    else:
        return render_template('deletecListItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showLearningCourses'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showLearningCourses'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
