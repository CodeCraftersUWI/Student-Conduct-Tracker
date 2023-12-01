import random
from flask import Blueprint, render_template, jsonify, get_flashed_messages
from App.models import db
from App.controllers import create_user, create_staff, create_student,create_review, get_latest_reviews, get_reviews_by_staff, get_staff, addVote
from flask_login import login_required, current_user
import randomname
import nltk
from nltk.corpus import names
import random

from App.models import Admin, Staff

index_views = Blueprint('index_views', __name__, template_folder='../templates')

def generate_random_contact_number():
    return f"0000-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Define a route for the index view
@index_views.route('/', methods=['GET'])
def index_page():
    db.drop_all()
    db.create_all()

    admin= create_user('bob', 'boblast' , 'bobpass')
    staff = create_staff(admin, "Jerrelle", "Johnson", "2", "2", "jerrelle9@icloud.com", 4)

    # nltk.download('names')

    male_names = names.words('male.txt')
    female_names = names.words('female.txt')

    all_names = male_names + female_names
    


    for student in range (2011, 2021): 
        create_student(admin, student, random.choice(all_names), random.choice(all_names),"Full-Time", 2)

    for staff in range (2000, 2010):
        create_staff(admin, random.choice(all_names), random.choice(all_names), "password2", str(staff), "staff@example.com", 5)
        create_review(staff, staff + 11, random.choice([True, False]), "reviewing...") 


    for staff in range(2000, 2010):
        reviews = get_reviews_by_staff(staff)

        if reviews:
            for review in reviews: 
                for voter in range(2000, 2010):
                    if get_staff(voter).ID != review.reviewerID: 
                        vote_type = random.choice(["upvote", "downvote"])  # Randomly select upvote/downvote
                        addVote(review.ID, get_staff(voter), vote_type)

                        

    
    return render_template('welcome.html')
    

@index_views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if not isinstance(current_user, Staff):
      return "Unauthorized", 401
    
    messages = get_flashed_messages()
    reviews = get_latest_reviews()

    if messages:
        return render_template('home.html', reviews=reviews, messages=messages)
    return render_template('home.html', reviews=reviews)