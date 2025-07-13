import uuid
from datetime import datetime, timedelta
from functools import wraps
import bcrypt
from flask import Blueprint, request, render_template, redirect, url_for, current_app, make_response
import jwt
from App.models.user import User
from App import mongo


auth = Blueprint('user', __name__, url_prefix='/')
@auth.route('/test')
def test_db():
    # print(mongo.db.list_collection_names())
    # mongo = current_app.extensions.get('pymongo')
    if not mongo:
        return "Mongo not initialized", 500
    try:
        collections = mongo.db.list_collection_names()
        return f"Collections: {collections}"
    except Exception as e:
        return f"Error: {str(e)}", 500

@auth.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'token' in request.cookies:
            token = request.cookies['token']
        if not token:
            return redirect(url_for('user.login'))
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"], options={"verify_exp": False})
        except:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html', title="Login", show_login=True, show_logout=False)
    if request.method == 'POST':
        form = request.form.get('form')
        login_ = 'login'
        register_ = 'register'
        if form == login_:
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            user = User.check_user(email, password, mongo)
            if user:
                token = jwt.encode({
                    'username': user.username,
                    'email': email,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                resp = make_response(redirect(url_for('user.home', username=user.username)))
                resp.set_cookie('token', token)
                return resp
        elif form == register_:
            custom_id = str(uuid.uuid4())
            username = request.form['username']
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user = User(custom_id, username, email, hashed_password)
            user.create_user(user, mongo)
            user = User.check_user(email, password, mongo)
            if user:
                token = jwt.encode({
                    'username': user.username,
                    'email': email,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                resp = make_response(redirect(url_for('user.home', username=user.username)))
                resp.set_cookie('token', token)
                return resp
            else:
                return render_template('user/login.html', title="Login", show_login=True, show_logout=False)
    return render_template('user/login.html', title="Login", show_login=True, show_logout=False)

@auth.route('/home/<username>', methods=['GET'])
@token_required
def home(username):
    try:
        token = request.cookies['token']
        user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"], options={"verify_exp": False})
        if user['username'] == username:
            return render_template('user/home.html', title="Home", user=user, show_login=False, show_logout=True)
        else:
            return redirect(url_for('user.logout'))
    except:
        return redirect(url_for('user.logout'))

@auth.route('/logout')
@token_required
def logout():
    resp = make_response(redirect(url_for('user.login')))
    resp.delete_cookie('token')
    return resp
