import sys
import time
from functools import wraps

from flask import Response, request, send_from_directory, render_template, jsonify, redirect, url_for, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import and_, or_

from libpass import app, db, login_manager
from libpass.models import *
from libpass.helper import *
from libpass.site_config import *



#################### Misc ####################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_redirect():
    return redirect('/login?url=' + request.path)


def return_error_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, __, exc_tb = sys.exc_info()
            return jsonify({'code': -1, 'error': '{}: {}'.format(e.__class__.__name__, e), 'line': exc_tb.tb_lineno})
    return wrapper


def return_error_html(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, __, exc_tb = sys.exc_info()
            return render_template('error.html', error_msg='({}) {}: {}'.format(exc_tb.tb_lineno, e.__class__.__name__, e))
    return wrapper


def browser_cache(seconds):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            if not isinstance(resp, Response):
                resp = make_response(resp)
            # Not setting 'Expires' because everyone is already using HTTP/1.1 now
            resp.headers['Cache-Control'] = 'public, max-age={}'.format(seconds)
            return resp
        return wrapper
    return outer_wrapper


#################### Web Pages ####################


@app.route('/')
@browser_cache(3600)
@return_error_html
def search_page():
    return render_template('main.html')


#################### APIs ####################


@app.route('/login', methods=['POST'])
@return_error_json
def login():
    '''
    API for login via the school's system.
    Response JSON: (code: int, msg: str, data: str)
        code: info code
            0: Success
            1: Invalid credentials
        msg: description of return code
        data: name of user
    '''

    # Get form data, defaults to empty string
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Attempt login
    ret, name = ykps_auth(username, password)

    # Construct response
    data = name if ret == 0 else ''
    msg = {
        0: 'Success',
        1: 'Invalid credentials'
    }.get(ret, '')

    return jsonify({'code': ret, 'msg': msg, 'data': data})


@app.route('/update-state', methods=['POST'])
@return_error_json
def update_state():
    '''
    API for updating the state of a student.
    Response JSON: (code: int, msg: str, data: str)
        code: info code
            0: Success
            1: Invalid credentials
        msg: description of return code
        data: name of user
    '''

    # Get form data
    student_id = request.form.get('id', '')
    new_state = request.form.get('state', '')

    # Perform some MySQL stuff here

    code = 0
    msg = {
        0: 'Success'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg})

