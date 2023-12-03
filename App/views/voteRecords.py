from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from App.controllers import Student, Staff, Review
from App.controllers.review import get_review
from App.controllers.voteRecords import (
    get_vote_records,
    get_votes_for_review,
    get_votes_by_staff,
    get_vote_record_by_staff_and_review,
    add_vote_record,
    delete_vote_record,
    edit_vote_record,
)
from App.database import db

vote_records_views = Blueprint('vote_records_views', __name__, template_folder='../templates')

# @vote_records_views.route('/vote-records', methods=['GET'])
# @jwt_required()
# def get_all_vote_records():
#     vote_records = get_vote_records()
#     return jsonify([vote_record.to_json() for vote_record in vote_records]), 200

# @vote_records_views.route('/vote-records/review/<int:review_id>', methods=['GET'])
# @jwt_required()
# def get_votes_for_review_action(review_id):
#     vote_records = get_votes_for_review(review_id)
#     return jsonify([vote_record.to_json() for vote_record in vote_records]), 200

# @vote_records_views.route('/vote-records/staff/<string:staff_id>', methods=['GET'])
# @jwt_required()
# def get_votes_by_staff_action(staff_id):
#     vote_records = get_votes_by_staff(staff_id)
#     return jsonify([vote_record.to_json() for vote_record in vote_records]), 200

# @vote_records_views.route('/vote-records/<string:staff_id>/<int:review_id>', methods=['GET'])
# @jwt_required()
# def get_vote_record_by_staff_and_review_action(staff_id, review_id):
#     vote_record = get_vote_record_by_staff_and_review(staff_id, review_id)
#     if vote_record:
#         return jsonify(vote_record.to_json()), 200
#     else:
#         return jsonify({"message": "Vote record not found"}), 404

# @vote_records_views.route('/vote-records/add', methods=['POST'])
# @jwt_required()
# def add_vote_record_action():
#     if not jwt_current_user or not isinstance(jwt_current_user, Staff):
#         return 'Unauthorized', 401

#     data = request.json
#     staff_id = jwt_current_user.ID
#     review_id = request.json['review_id']
#     vote_type = request.json['vote_type']

#     if not review_id or not vote_type:
#         return "Invalid request data", 400

#     review = get_review(review_id)
#     if not review:
#         return "Review not found", 404

#     vote_record = get_vote_record_by_staff_and_review(staff_id, review_id)

#     if vote_record:
#         return jsonify({"message": "Vote record already exists."}), 400

#     vote_record = add_vote_record(staff_id, review_id, vote_type)

#     if vote_record:
#         return jsonify(vote_record.to_json()), 201
#     return 'Failed to add vote record', 400

# @vote_records_views.route('/vote-records/edit/<string:staff_id>/<int:review_id>', methods=['PUT'])
# @jwt_required()
# def edit_vote_record_action(staff_id, review_id):
#     if not jwt_current_user or not isinstance(jwt_current_user, Staff):
#         return 'Unauthorized', 401

#     data = request.json
#     new_type = request.json['new_type']

#     if not new_type:
#         return "Invalid request data", 400

#     vote_record = edit_vote_record(staff_id, review_id, new_type)

#     if vote_record:
#         return jsonify(vote_record.to_json()), 200
#     else:
#         return jsonify({"message": "Vote record not found or failed to edit"}), 404

# @vote_records_views.route('/vote-records/delete/<string:staff_id>/<int:review_id>', methods=['DELETE'])
# @jwt_required()
# def delete_vote_record_action(staff_id, review_id):
#     if not jwt_current_user or not isinstance(jwt_current_user, Staff):
#         return 'Unauthorized', 401

#     vote_record = get_vote_record_by_staff_and_review(staff_id, review_id)

#     if vote_record:
#         delete_vote_record(vote_record)
#         return jsonify({"message": "Vote record deleted successfully"}), 200
#     else:
#         return jsonify({"message": "Vote record not found or failed to delete"}), 404