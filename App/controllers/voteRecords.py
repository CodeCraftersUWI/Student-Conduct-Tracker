import datetime
from App.models import VoteRecord, Karma, Student
from App.database import db

def get_vote_records():
    return db.session.query(VoteRecord).all()

def get_votes_for_review(review_id):
    return db.session.query(VoteRecord).filter_by(review_id=review_id).all()

def get_votes_by_staff(staff_id):
    return db.session.query(VoteRecord).filter_by(staff_id=staff_id).all()

def add_vote_record(staff_id, review_id, vote_type):
    vote_record = VoteRecord(staff_id=staff_id, review_id=review_id, type=vote_type)
    db.session.add(vote_record)
    db.session.commit()
    return vote_record

def delete_vote_record(vote_record):
    db.session.delete(vote_record)
    db.session.commit()
    return True

def edit_vote_record(vote_record, new_type):
    if new_type.lower() == 'upvote':
        vote_record.type = 'upvote'
    elif new_type.lower() == 'downvote':
        vote_record.type = 'downvote'
    else:
        return None

    vote_record.voted_at = datetime.utcnow()

    db.session.add(vote_record)
    db.session.commit()
    return vote_record

