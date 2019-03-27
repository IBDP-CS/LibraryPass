import time

from flask import Flask, request, jsonify

from helper import *


app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    '''API for'''

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
def update_state():
    # Get form data
    student_id = request.form.get('id', '')
    new_state = request.form.get('state', '')

    # Perform some MySQL stuff here

    code = 0
    msg = {
        0: 'Success'
    }.get(code, '')

    return jsonify({'code': code, 'msg': msg})
