from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from App.database import db
from App.controllers import Student
from App.models import Staff

from App.controllers.karma import (
    update_student_karma_rankings,
)

# Create a Blueprint for karma views
karma_views = Blueprint("karma_views", __name__, template_folder='../templates')

# Route to update Karma rankings for all students
@karma_views.route("/karma/update_rankings", methods=["POST"])
@login_required
def update_karma_rankings_route():
    if not isinstance(current_user, Staff):
      return "Unauthorized", 401
    
    update_student_karma_rankings()
    return "Karma rankings updated", 200
