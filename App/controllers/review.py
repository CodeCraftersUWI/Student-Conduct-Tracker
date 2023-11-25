from App.models import Review, Karma, Student, VoteRecords
from App.controllers.voteRecords import edit_vote_record, add_vote_record, get_vote_record_by_staff_and_review
from App.database import db

def get_reviews(): 
    return db.session.query(Review).all()

def get_reviews_for_student(studentID):
    return db.session.query(Review).filter_by(studentID=studentID).all()

def get_review(reviewID):
    return Review.query.filter_by(ID=reviewID).first()

def get_reviews_by_staff(staffID):
    return db.session.query(Review).filter_by(reviewerID=staffID).all()


def edit_review(review, staff, is_positive, comment):
    if review.reviewer == staff:
        review.isPositive = is_positive
        review.comment = comment
        db.session.add(review)
        db.session.commit()
        return review
    return None


def delete_review(review, staff):
    if review.reviewer == staff:
        db.session.delete(review)
        db.session.commit()
        return True
    return None


def addVote(reviewID, staff, type):
    review = get_review(reviewID)

    if review:
        if review.voters is None: # checks if staff member voted already
            voteRecord = get_vote_record_by_staff_and_review(staff.id, reviewID) # need to see what staff previously voted for

            if voteRecord.type == "upvote" and type == "upvote": # if staff wants to upvote again and they already upvoted, nothing just return
                return review.upvotes
            
            if voteRecord.type == "downvote" and type == "downvote": # if staff wants to downvote again and they already downvoted, nothing just return
                return review.downvotes
            
            ##current record is a downvote but staff wants to change upvote
            if voteRecord.type == "downvote" and type == "upvote":
                review.downvotes -= 1
                review.upvotes += 1
                edit_vote_record(staff, "upvote")
                db.session.add(review)
                db.session.commit()
                updateKarma(review)
                return review.upvotes

            #current record is upvote but staff wants to change downvote
            if voteRecord.type == "upvote" and type == "downvote":
                review.upvotes -= 1
                review.downvotes += 1
                edit_vote_record(staff, "upvote")
                db.session.add(review)
                db.session.commit()
                updateKarma(review)
                return review.downvotes  
        else: # staff first time voting
            add_vote_record(staff.get_id(), reviewID, type)
            review.voters.append(staff)
            if type == "upvote":
                review.upvotes += 1
            else:
                review.downvotes += 1
            
            updateKarma(review)
            db.session.add(review)
            db.session.commit()
    else:
        return


def updateKarma(review): 
    # Retrieve the associated Student object using studentID
    student = db.session.query(Student).get(review.studentID)

    # Check if the student has a Karma record (karmaID) and create a new Karma record for them if not
    if student.karmaID is None:
        karma = Karma(score=0.0, rank=-99)
        db.session.add(karma)  # Add the Karma record to the session
        db.session.flush()  # Ensure the Karma record gets an ID
        db.session.commit()
        # Set the student's karmaID to the new Karma record's ID
        student.karmaID = karma.karmaID

    # Update Karma for the student
    student_karma = db.session.query(Karma).get(student.karmaID)
    student_karma.calculateScore(student)
    student_karma.updateRank()