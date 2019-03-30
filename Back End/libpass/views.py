import re
import sys
import time
import traceback
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
            # Returning the line number of the immediate cause, not the root cause
            return jsonify({'code': -1, 'error': '{}: {}'.format(e.__class__.__name__, e), 'line': traceback.extract_tb(exc_tb)[1].lineno})
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

    name = ''
    if not all((username, password)): # Data validation
        code = 1
    else:
        # Try fetching user from database
        user = User.query.filter_by(school_id=username).first()

        # If user is already in the database, validate credentials directly
        if user:
            if user.authenticate(password):
                code = 0
                name = user.name
            else:
                code = 1

        # New user trying to log in
        else:
            # Authenticate via PowerSchool
            code, name = ykps_auth(username, password)

            if code == 0:
                # User credentials validated, insert into database
                hashed_password = generate_password_hash(password)
                is_student = bool(re.match(r's\d{5}', username))
                user = User(school_id=username, name=name, password=hashed_password, is_student=is_student)
                db.session.add(user)
                db.session.commit()
                state = State(school_id=username)
                db.session.add(state)
                db.session.commit()

    if code == 0:
        # User credentials validated, logs in the user
        login_user(user)

    # Construct response
    msg = {
        0: 'Success',
        1: 'Invalid credentials'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg, 'data': name})


@app.route('/update-state', methods=['POST'])
@return_error_json
def update_state():
    '''
    API for updating the state of a student.
    Response JSON: (code: int, msg: str)
        code: info code
            0: Success
            1: Invalid parameters
        msg: description of return code
    '''

    # Get form data
    student_id = request.form.get('id', '')
    new_state = request.form.get('state', '')

    if not (all((student_id, new_state)) and new_state.isdigit() and int(new_state) in range(5)): # Data validation
        code = 1
    else:
        # Further data validations
        student = User.query.filter_by(school_id=student_id).first()
        if not (student and student.is_student):
            code = 1
        else:
            new_state = int(new_state)
            current_state = State.query.filter_by(school_id=student_id).first()
            if (new_state - current_state.state) % 5 != 1:
                # Skipping state transitions
                code = 1
            else:
                # All validations passed, update state
                code = 0
                current_state.state = new_state
                db.session.commit()

    # Construct response
    msg = {
        0: 'Success',
        1: 'Invalid parameters'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg})

