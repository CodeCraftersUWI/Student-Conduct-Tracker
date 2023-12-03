import datetime
from App.models import VoteRecords, Karma, Student
from App.database import db

def get_vote_records():
    return db.session.query(VoteRecords).all()

def get_votes_for_review(review_id):
    return db.session.query(VoteRecords).filter_by(review_id=review_id).all()

def get_votes_by_staff(staff_id):
    return db.session.query(VoteRecords).filter_by(staff_id=staff_id).all()

def get_vote_record_by_staff_and_review(staff_id, review_id):
    return VoteRecords.query.filter_by(staff_id=staff_id, review_id=review_id).first()

def add_vote_record(staff_id, review_id, vote_type):
    vote_record = VoteRecords(staff_id=staff_id, review_id=review_id, type=vote_type)
    db.session.add(vote_record)
    db.session.commit()
    return vote_record

def delete_vote_record(vote_record):
    db.session.delete(vote_record)
    db.session.commit()
    return True

def edit_vote_record(staff_id, review_id, new_type):
    voted_record = VoteRecords.query.filter_by(staff_id=staff_id, review_id=review_id).first()
    if voted_record:
        if new_type.lower() == 'upvote':
            voted_record.type = 'upvote'
        elif new_type.lower() == 'downvote':
            voted_record.type = 'downvote'
        else:
            return None

        voted_record.voted_at = datetime.datetime.utcnow()

        db.session.add(voted_record)
        db.session.commit()

        return voted_record
    return None

