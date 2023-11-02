from bottle import Bottle, \
    jinja2_template as template, \
        static_file, request, redirect

from bottle import Bottle,response, run, TEMPLATE_PATH
import routes
from models import connection, BookUser
from utils.session import Session
from utils.auth import Auth
import urllib.parse as urlpar
import os

REDIRECT_AFTER_LOGIN = '/list'
REDIRECT_AFTER_LOGOFF = '/'
TEMPLATE_PATH.append(os.path.abspath('user/views'))

app = routes.app

@app.route('/') 
def index():
    err_msg = request.query.error
    if err_msg is None:
        err_msg = None
    return template('login.html', error= err_msg)


@app.route('/login', method='POST') 
def login():
    user_id = request.forms.decode().get('user_id')
    passwd = request.forms.decode().get('passwd')
    
    user = connection.query(BookUser.user_id).filter \
        (BookUser.user_id == user_id, \
            BookUser.passwd == passwd, \
                BookUser.delFlg == False).scalar()
    print(user)
    if user is not None:
        auth = Auth()
        auth.add_auth(user)
        redirect(REDIRECT_AFTER_LOGIN)
    else:
        err_msg = urlpar.quote('認識に失敗しました')
        redirect(REDIRECT_AFTER_LOGOFF + '?error=' + err_msg )
        
@app.route('/logout', method=['GET', 'POST']) 
def logout():
    auth = Auth()
    auth.del_auth()
    redirect(REDIRECT_AFTER_LOGOFF)