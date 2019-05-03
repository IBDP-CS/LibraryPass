import re
import sys
import traceback
from functools import wraps

from flask import Response, request, render_template, jsonify
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash

from libpass import app, db, login_manager
from libpass.models import *
from libpass.helper import *



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



#################### Web Pages ####################

@app.route('/')
def index_page():
    # Return login page if not logged in
    if not current_user.is_authenticated:
        return render_template('login.html')

    # Return corresponding pages
    if current_user.user_type == 0:
        return render_template('student.html')
    elif current_user.user_type == 1:
        return render_template('dorm.html')
    elif current_user.user_type == 2:
        return render_template('library.html')



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
                user_type = 0 if re.match(r's\d{5}', username) else 1
                user = User(school_id=username, name=name, password=hashed_password, user_type=user_type)
                db.session.add(user)
                db.session.commit()
                if user_type == 0:
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
        # Further data validationsg
        student = User.query.filter_by(school_id=student_id).first()
        if not (student and student.user_type == 0):
            code = 1
        else:
            new_state = int(new_state)
            student_state = State.query.filter_by(school_id=student_id).first()

            if app.config['ENV'] == 'production':
                # Make sure state transition is valid
                if (new_state - student_state.state) % 5 != 1 and not (student_state.state == 1 and new_state == 0):
                    # Skipping state transitions
                    code = 1
                else:
                    # All validations passed, update state
                    code = 0
                    student_state.state = new_state
                    db.session.commit()

            elif app.config['ENV'] == 'development':
                # Ignore state transition check for the sake of development
                code = 0
                student_state.state = new_state
                db.session.commit()

    # Construct response
    msg = {
        0: 'Success',
        1: 'Invalid parameters'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg})


@app.route('/get-state', methods=['POST'])
@return_error_json
def get_student_state():
    '''
    API for getting the state of a specific student.
    Response JSON: (code: int, msg: str, data: int)
        code: info code
            0: Success
            1: Invalid parameters
        msg: description of return code
        data: the state code of the student
    '''

    # Get form data
    student_id = request.form.get('id', '')

    current_state = -1
    # Data validation
    if not student_id:
        code = 1
    else:
        # Further data validations
        student = User.query.filter_by(school_id=student_id).first()
        if not (student and student.user_type == 0):
            code = 1
        else:
            # Get the state of the student
            current_state = State.query.filter_by(school_id=student_id).first().state
            code = 0

    # Construct response
    msg = {
        0: 'Success',
        1: 'Invalid parameters'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg, 'data': current_state})


@app.route('/get-students', methods=['POST'])
@return_error_json
def get_state_students():
    '''
    API for getting a list of students at a specific state.
    Response JSON: (code: int, msg: str, data: list[])
        code: info code
            0: Success
            1: Invalid parameters
        msg: description of return code
        data:
        [
          {
            id[str]: student ID of the student,
            name[str]: name of the student
            ts[int]: timestamp of this student's last update
          },
          ...
        ]
    '''

    # Get form data
    state = request.form.get('state', '')

    # Data validation
    if not (state.isdigit() and int(state) in range(5)):
        code = 1
    else:
        state = int(state)

        # Fetch results from database
        students = State.query.filter_by(state=state).all()
        results = []
        for student in students:
            school_id = student.school_id
            student_name = User.query.filter_by(school_id=school_id).first().name
            results.append({'id': school_id, 'name': student_name, 'ts': student.updated.timestamp()})

        code = 0

    # Construct response
    msg = {
        0: 'Success',
        1: 'Invalid parameters'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg, 'data': results})
