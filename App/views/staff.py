import random
import string
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from App.controllers import Student, Staff
from App.controllers.user import get_staff, get_student
from App.database import db
from flask_login import login_required, current_user
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required

from App.controllers.staff import (
    search_students_searchTerm, 
    get_student_rankings,
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/rankings', methods=['GET'])
@login_required
def get_karma_rankings():
  if not isinstance(current_user, Staff):
    return "Unauthorized", 401
  
  rankings = get_student_rankings(current_user)
  return render_template('topranking.html', rankings=rankings)
  

@staff_views.route('/new_review', methods=['POST', 'GET'])
@login_required
def newReview():

  if not isinstance(current_user, Staff):
    return "Unauthorized", 401
  
  if request.method == 'POST':

    staff_id = current_user.get_id()
    student_id = request.form['studentID']

    student = get_student(student_id)
    if not student:
      flash("Student ID not found")
      return redirect('/new_review')
    

    review_type = request.form['reviewType']
    description = request.form['description']
    if review_type == "Positive":
      is_positive = True
    else:
      is_positive = False

    review = create_review(staff_id, student_id, is_positive, description)
    return redirect(f"/review_details/{review.ID}")
    
  return render_template('createreview.html')

# @staff_views.route('/staff/<string:staff_id>', methods=['GET'])
# def get_staff_action(staff_id):
#     staff = get_staff(str(staff_id))
#     if staff:
#         return jsonify(staff.to_json())
#     return 'Staff not found', 404

# @staff_views.route('/students/<string:student_id>/reviews', methods=['POST'])
# @jwt_required()
# def create_review_action(student_id):
#     if not jwt_current_user or not isinstance(jwt_current_user, Staff):
#       return 'Unauthorized', 401

#     student= get_student(str(student_id))

#     if not student:
#         return jsonify({"error": 'Student does not exist'}), 404

#     data = request.json
#     if not data['comment']:
#         return "Invalid request data", 400
    
#     if data['isPositive'] not in (True, False):
#         return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

#     if not get_staff(str(jwt_current_user.ID)):
#         return 'Staff does not exist', 404 

#     review = create_review(jwt_current_user.ID, student_id, data['isPositive'], data['comment'])
    
#     if review:
#         return jsonify(review.to_json()), 201
#     return 'Failed to create review', 400

# @staff_views.route('/students/search/<string:search_term>', methods=['GET'])
# @jwt_required()
# def search_students(search_term):
#   if jwt_current_user and isinstance(jwt_current_user, Staff): 
#     students = search_students_searchTerm(jwt_current_user, search_term)
#     if students:
#       return jsonify([student for student in students]), 200
#     else:
#       return jsonify({"message": f"No students found with search term {search_term}"}), 204
#   else:
#     return jsonify({"message": "You are not authorized to perform this action"}), 401


  
  
  