from flask import request,render_template,session
from dashboard import app
from dashboard.model import user as user_model
from dashboard.model import contact as contact_model
from bson.objectid import ObjectId
from dashboard.model import db


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        user_details = user_model.search_by_user_id(session['user_id'])
        return render_template('home.html',name = user_details['name'])
    else:
        return render_template('index.html', message='login to contact')


@app.route('/api/logout',methods=['GET'])
def remove():
    session.clear()
    return render_template('index.html',message = 'succesfully logged out')


@app.route('/api/user',methods=['GET','POST'])
def user():

    op_type = request.form['op_type']
    if op_type == 'login':
        username = request.form['username']
        password = request.form['password']
        success = user_model.authenticate(username, password)
        if success:
            user_details = user_model.search_by_username(username)
            session['user_id'] = str(user_details['_id'])
            return render_template('home.html', message='sucessfull login')
        else:
            return render_template('index.html', message='unsucessfull login')

    elif op_type == 'signup':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        success = user_model.signup_user(name, username, password)
        if success:
            user_details = user_model.search_by_username(username)
            session['user_id'] = str(user_details['_id'])
            return render_template('home.html', message='signed up')
        else:
            return render_template('index.html', message='username exists')
    else:

        return render_template('index.html', message='some_wrong')


@app.route('/api/contact_form',methods=['GET'])
def contact_form():
    return render_template('contact_form.html')


@app.route('/api/jobfeild',methods=['GET'])
def jobfeild():
    query = {'user_id': session['user_id']}
    cursor = db.contacts.find(query)
    if cursor.count() == 1:
        user_data = cursor[0]
        return render_template('jobfeild.html',data= user_data)


@app.route('/api/personal_data',methods=['GET'])
def personal_data():
    query = {'user_id' : session['user_id']}
    cursor = db.contacts.find(query)
    if cursor.count() == 1:
        user_data = cursor[0]
        data = {
            'name' : user_data['name'],
            'email': user_data['email'],
            'number': user_data['number']
        }
        return render_template('personal_data.html', data = data)
    else:
        return None



@app.route('/api/contact_details',methods = ['POST'])
def contact_details():
    user = {
         'name' : request.form['name'],
         'email' : request.form['email'],
         'number' : request.form['number'],
         'jobfeild' : request.form['jobfeild'],
         'user_id':  session['user_id']
    }
    sucesss = contact_model.add_contact(user)
    if sucesss:
        return render_template('home.html', message='contact added')
    else:
        return render_template('home.html', message='unable to add contact or contact already exists')



