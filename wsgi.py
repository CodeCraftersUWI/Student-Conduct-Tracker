from App.views.index import generate_random_contact_number
import click, pytest, sys
from flask import Flask, jsonify
from flask.cli import with_appcontext, AppGroup
import random
import randomname
from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, create_staff, create_review, create_student, get_all_users_json, get_all_users, addVote, get_staff, add_vote_record )
from App.views import (generate_random_contact_number)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  admin= create_user('bob', 'boblast' , 'bobpass')
  for ID in  range(2, 50): 
    staff= create_staff(admin, 
          randomname.get_name(), 
          randomname.get_name(), 
          randomname.get_name(), 
          str(ID), 
          randomname.get_name() + '@schooling.com', 
          str(random.randint(1, 15))
      )
    db.session.add(staff)
    db.session.commit()

  for ID in range(50, 150): 
      contact= generate_random_contact_number()
      student= create_student(admin, str(ID),
          randomname.get_name(), 
          randomname.get_name(),
          contact,
          random.choice(['Full-Time','Part-Time', 'Evening']),
          str(random.randint(1, 8))
      )
      db.session.add(student)
      db.session.commit()

  staff= create_staff(admin, 
          "stafftester", 
          randomname.get_name(), 
          "bobpass", 
          str(ID), 
          randomname.get_name() + '@schooling.com', 
          str(random.randint(1, 15))
    )
  db.session.add(staff)
  db.session.commit()
  review = create_review(2, 50, True, "Testing")
  vote_record = addVote(1, staff, "upvote")

  return jsonify({'message': 'Database initialized'}),201

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("firstname", default="rob")
@click.argument("password", default="robpass")
def create_user_command(firstname, password):
    create_user(firstname, password)
    print(f'{firstname} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("review", help="Create a review")
def createReview():
    # create_review(2, 51, True, "Good Job")
    staff = get_staff(2)
    addVote(1, staff, "downvote")


@user_cli.command("testing", help="Create a review")
def test():
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
    

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)