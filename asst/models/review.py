'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class review(UserMixin, BaseModel):
    class Meta:
        db_table = 'writes_review'
    '''A User model for who will be using the software. Users have different levels of access with different roles
    Current active roles:
        - customer
        - manager
    '''
    ReviewID = IntegerField(primary_key=True)
    Rating = IntegerField()
    TextComment = CharField()
    CID = IntegerField()




    @classmethod
    def write_review(cls, reviewID, rating, text_comment, cid):
        '''writes a review
        Args:
            reviewID : Identification of the review
            rating : score the customer gives
            TextComment : textual description customer gives
            CID : customer identification
        Returns:
            N/A
        Raises:
            ValueError: When cid already exists
        '''

        try:
            cls.create(
                ReviewID = reviewID,
                Rating = rating,
                TextComment = text_comment,
                CID = cid)
        except IntegrityError:
            raise ValueError("Review already exists")
