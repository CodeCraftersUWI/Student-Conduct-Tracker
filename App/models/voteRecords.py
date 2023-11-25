from App.database import db
from datetime import datetime

class VoteRecords(db.Model):
    __tablename__ = 'vote_records'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.ID'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.ID'))
    type = db.Column(db.String, nullable=False)  # 'upvote' or 'downvote'
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

#staff = db.relationship('Staff', backref=db.backref('vote_records', lazy='dynamic'), foreign_keys=[staff_id])

    def __init__(self, staff_id, review_id, type):
        self.staff_id = staff_id
        self.review_id = review_id
        self.type = type

    def to_json(self):
        return {
            "id": self.id,
            "staff_id": self.staff_id,
            "review_id": self.review_id,
            "type": self.type,
            "voted_at": self.voted_at.strftime("%d-%m-%Y %H:%M")
        }

    # @classmethod
    def get_votes_for_review(cls, review_id):
        # Method to get all votes for a specific review
        return cls.query.filter_by(review_id=review_id).all()

    def get_votes_by_staff(cls, staff_id):
        # Method to get all votes cast by a specific staff member
        return cls.query.filter_by(staff_id=staff_id).all()
