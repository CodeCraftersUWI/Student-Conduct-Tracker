import ast
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session, get_flashed_messages
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta

from.index import index_views
from App.models import Staff, Admin

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_authenticate_admin,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/login', methods=['POST', 'GET'])
def login_action():
    if request.method == 'POST':
        data = request.form
        user_id = data.get('ID')  # Get the entered ID
        password = data.get('password')  # Get the entered password

        user = login(user_id, password)
        if user:
            if isinstance(user, Staff):
                session['logged_in'] = True
                login_user(user)
                return redirect('/home')
            
            message = {"message": "Admin successfully logged in"}
            return jsonify(message), 200
        
        
        flash('Invalid username or password')
        # error_message = 'Incorrect ID or password given'
        # return jsonify({'error': error_message}), 401
        return redirect('/login')
    
    messages = get_flashed_messages()
    return render_template('login.html', messages=messages)


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('auth_views.login_action', _external=True))
    # return redirect(('/login'))
   

# @auth_views.route('/api/login', methods=['POST'])
# def user_login_api():
# 	data = request.json
# 	token = jwt_authenticate(data['ID'], data['password'])
# 	if not token:
# 		return jsonify(message='bad username or password given'), 401
# 	return jsonify(access_token=token)

# @auth_views.route('/api/admin/login', methods=['POST'])
# def admin_login_api():
#   data = request.json
#   token = jwt_authenticate_admin(data['ID'], data['password'])
#   if not token:
#     return jsonify(message='bad username or password given'), 401
#   return jsonify(access_token=token)


# @auth_views.route('/api/identify', methods=['GET'])
# @jwt_required()
# def identify_user_action():
#     return jsonify({'message': f"firstname: {jwt_current_user.firstname}, lastname: {jwt_current_user.lastname}, id : {jwt_current_user.ID}"})
