from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required, current_user
from App.controllers import Review, Staff
from App.controllers.user import get_staff
from App.controllers.student import search_student
from App.controllers.voteRecords import get_vote_record_by_staff_and_review


from App.controllers.review import (
    get_reviews_by_staff,
    edit_review,
    delete_review,
    get_reviews,
    get_reviews_for_student, 
    get_review,
    addVote
)

# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

# Route to list all reviews (you can customize this route as needed)
@review_views.route('/review_details/<int:review_id>', methods=['GET', 'POST'])
@login_required
def view_review(review_id):
    if not isinstance(current_user, Staff):
        return "Unauthorized", 401
    
    if request.method == "POST":
        vote_type = request.json.get('action')
        addVote(review_id, current_user, vote_type)
        updated_review = get_review(review_id)
        return jsonify({'upvotes': updated_review.upvotes, 'downvotes': updated_review.downvotes})
        # return redirect(url_for('review_views.view_review', review_id=review_id))

    review = get_review(review_id)
    if review:
        return render_template('reviewdetails.html', review_id=review_id, review = review) 
        

    
    



#Route to upvote review 
@review_views.route('/review/<int:review_id>/upvote', methods=['POST'])
@jwt_required()
def upvote (review_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return "You are not authorized to upvote this review", 401
      
    vote_type = "upvote"
    review = get_review(review_id)
    staff = get_staff(jwt_current_user.ID)
    if review:
        # Check if staff member already voted
        vote_record = get_vote_record_by_staff_and_review(staff.ID, review_id)
        if vote_record:
            # Staff has voted before
            if vote_record.type == vote_type:
                # Staff wants to vote the same way they voted before, return current votes
                return jsonify(review.to_json(), 'Review Already Upvoted'), 201 
            else:
                new_votes= addVote(review_id, staff, vote_type)
                return jsonify(review.to_json(), 'Review Upvoted'), 200
        else:
            new_votes= addVote(review_id, staff, vote_type)
            return jsonify(review.to_json(), 'Review Upvoted'), 200
    else:
        return 'Review does not exist', 404



#Route to downvote review 
@review_views.route('/review/<int:review_id>/downvote', methods=['POST'])
@jwt_required()
def downvote (review_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return "You are not authorized to downvote this review", 401
  
    vote_type = "downvote"
    review = get_review(review_id)
    staff = get_staff(jwt_current_user.ID)
    if review:
        # Check if staff member already voted
        vote_record = get_vote_record_by_staff_and_review(staff.ID, review_id)
        if vote_record:
            if vote_record.type == vote_type:
                # Staff wants to vote the same way they voted before, return current votes
                return jsonify(review.to_json(), 'Review Already Downvoted'), 201 
            else:
                new_votes= addVote(review_id, staff, vote_type)
                return jsonify(review.to_json(), 'Review Downvoted'), 200
        else:
            new_votes= addVote(review_id, staff, vote_type)
            return jsonify(review.to_json(), 'Review Downvoted'), 200
    else:
        return 'Review does not exist', 404

# Route to get reviews by student ID
@review_views.route("/student/<string:student_id>/reviews", methods=["GET"])
def get_reviews_of_student(student_id):
    if search_student(student_id):
        reviews = get_reviews_for_student(student_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found for the student", 404
    return "Student does not exist", 404

# Route to get reviews by staff ID
@review_views.route("/staff/<string:staff_id>/reviews", methods=["GET"])
def get_reviews_from_staff(staff_id):
    if get_staff(str(staff_id)):
        reviews = get_reviews_by_staff(staff_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found by the staff member", 404
    return "Staff does not exist", 404

# # Route to edit a review
# @review_views.route("/reviews/edit/<int:review_id>", methods=["PUT"])
# @jwt_required()
# def review_edit(review_id):
#     review = get_review(review_id)
#     if not review:
#       return "Review not found", 404
      
    if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
      return "You are not authorized to edit this review", 401

    staff = get_staff(jwt_current_user.ID)

    data = request.json

    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity value  ({data['isPositive']}). Positive: true or false"}), 400

    updated= edit_review(review, staff, data['isPositive'], data['comment'])
    if updated: 
      return jsonify(review.to_json(), 'Review Edited'), 200
    else:
      return "Error updating review", 400



# # Route to delete a review
# @review_views.route("/reviews/delete/<int:review_id>", methods=["DELETE"])
# @jwt_required()
# def review_delete(review_id):
#     review = get_review(review_id)
#     if not review:
#       return "Review not found", 404

    if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
      return "You are not authorized to delete this review", 401

    staff = get_staff(jwt_current_user.ID)
   
    if delete_review(review, staff):
        return "Review deleted successfully", 200
    else:
        return "Issue deleting review", 400

