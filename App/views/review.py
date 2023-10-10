from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user
from App.controllers import Review

from App.controllers.review import (
    get_reviews_by_student,
    get_reviews_by_staff,
    edit_review,
    delete_review,
    upvoteReview,
    downvoteReview,
)

# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

# Route to list all reviews (you can customize this route as needed)
@review_views.route('/reviews')
@jwt_required()
def list_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_json() for review in reviews]), 200

# Route to view a specific review and vote on it
@review_views.route('/review/<int:review_id>', methods=['GET', 'POST'])
@jwt_required()
def view_review(review_id):
    review = Review.query.get(review_id)

    if request.method == 'POST':
        if 'upvote' in request.form:
            upvoteReview(review_id, current_user)
        elif 'downvote' in request.form:
            downvoteReview(review_id, current_user) 

        # Redirect back to the review after voting
        return redirect(url_for('view_review', review_id=review_id))

    return render_template('view_review.html', review=review)

# Route to get reviews by student ID
@review_views.route("/reviews/student/<string:student_id>", methods=["GET"])
@jwt_required()
def get_reviews_for_student(student_id):
    reviews = get_reviews_by_student(student_id)
    if reviews:
        return jsonify([review.to_json() for review in reviews]), 200
    else:
        return "No reviews found for the student", 404

# Route to get reviews by staff ID
@review_views.route("/reviews/staff/<string:staff_id>", methods=["GET"])
@jwt_required()
def get_reviews_from_staff(staff_id):
    reviews = get_reviews_by_staff(staff_id)
    if reviews:
        return jsonify([review.to_json() for review in reviews]), 200
    else:
        return "No reviews found by the staff member", 404

# Route to edit a review
@review_views.route("/reviews/edit/<int:review_id>", methods=["PUT"])
@jwt_required()
def review_edit(review_id):
    review = Review.query.get(review_id)
    if not review:
        return "Review not found", 404

    if jwt_current_user.is_authenticated and current_user == review.reviewer:
        data = request.get_json()
        is_positive = data.get("isPositive")
        comment = data.get("comment")
        if is_positive is not None and comment is not None:
            edit_review(review, current_user, is_positive, comment)
            return jsonify(review.to_json()), 200
        else:
            return "Invalid request data", 400
    else:
        return "Unauthorized to edit this review", 401

# Route to delete a review
@review_views.route("/reviews/delete/<int:review_id>", methods=["DELETE"])
@jwt_required()
def review_delete(review_id):
    review = Review.query.get(review_id)
    if not review:
        return "Review not found", 404

    if current_user.is_authenticated and current_user == review.reviewer:
        delete_review(review, current_user)
        return "Review deleted successfully", 200
    else:
        return "Unauthorized to delete this review", 401
