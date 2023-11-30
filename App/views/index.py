import random
from flask import Blueprint, render_template, jsonify, get_flashed_messages
from App.models import db
from App.controllers import create_user, create_staff, create_student,create_review, get_latest_reviews
from flask_login import login_required
import randomname

from App.models.admin import Admin

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

    for ID in range(816029801, 816029811): 
        contact= generate_random_contact_number()
        student= create_student(admin, str(ID),
            randomname.get_name(), 
            randomname.get_name(),
            contact,
            random.choice(['Full-Time','Part-Time', 'Evening']),
            str(random.randint(1, 8))
        )
        create_review(staff.ID, ID, random.choice([True, False]), "reviewing...") 
        db.session.add(student)
        db.session.commit()

    # for ID in  range(3, 50): 
    #     staff= create_staff(admin, 
    #         randomname.get_name(), 
    #         randomname.get_name(), 
    #         randomname.get_name(), 
    #         str(ID),
    #         randomname.get_name() + '@schooling.com', 
    #         str(random.randint(1, 15))
    #     )
    #     db.session.add(staff)
    #     db.session.commit()

    
    return render_template('welcome.html')
    

@index_views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    messages = get_flashed_messages()
    reviews = get_latest_reviews()

    if messages:
        return render_template('home.html', reviews=reviews, messages=messages)
    return render_template('home.html', reviews=reviews)