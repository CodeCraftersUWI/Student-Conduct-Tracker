from App.database import db
from .student import Student
from datetime import datetime
from .karma import Karma
from .voteRecords import VoteRecords

class Review(db.Model):
  __tablename__ = 'review'
  ID = db.Column(db.Integer, primary_key=True)
  reviewerID = db.Column(
      db.String(10),
      db.ForeignKey('staff.ID'))  #each review has 1 creator

  #create reverse relationship from Staff back to Review to access reviews created by a specific staff member
  reviewer = db.relationship('Staff',
                             backref=db.backref('reviews_created',
                                                lazy='joined'),
                             foreign_keys=[reviewerID])

  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  
  voters = db.relationship(
      'Staff',
      secondary = 'vote_records',
      backref=db.backref(
          'vote_records',
          lazy='joined')) 

  upvotes = db.Column(db.Integer, nullable=False)
  downvotes = db.Column(db.Integer, nullable=False)
  isPositive = db.Column(db.Boolean, nullable=False)
  created = db.Column(db.DateTime, default=datetime.utcnow)
  comment = db.Column(db.String(400), nullable=False)

  # initialize the review. when it is created the date is automatically gotten and votes are at 0
  def __init__(self, reviewer, student, isPositive, comment):
    self.reviewerID = reviewer.ID
    self.reviewer = reviewer
    self.studentID = student.ID
    self.isPositive = isPositive
    self.comment = comment
    self.upvotes = 0
    self.downvotes = 0
    self.created = datetime.now()

  def get_id(self):
    return self.ID


#allows the comment and whether the review is positive to be edited if the staff member is the creator of the review, returns none if not

  def editReview(self, staff, isPositive, comment):
    if self.reviewer == staff:
      self.isPositive = isPositive
      self.comment = comment
      db.session.add(self)
      db.session.commit()
      return True
    return None

  #deletes the review when called if the staff memeber is the creator of the review, return none if not

  def deleteReview(self, staff):
    if self.reviewer == staff:
      db.session.delete(self)
      db.session.commit()
      return True
    return None

  def to_json(self):
    return {
        "reviewID": self.ID,
        "reviewer": self.reviewer.firstname + " " + self.reviewer.lastname,
        "studentID": self.student.ID,
        "studentName": self.student.firstname + " " + self.student.lastname,
        "created":
        self.created.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        "isPositive": self.isPositive,
        "upvotes": self.upvotes,
        "downvotes": self.downvotes,
        "comment": self.comment
    }
  
  
