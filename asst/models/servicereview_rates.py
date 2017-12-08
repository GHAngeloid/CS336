'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class ServiceReview_rates(UserMixin, BaseModel):
    class Meta:
        db_table = 'ServiceReview_rates'
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    ReviewID = IntegerField(primary_key=True)
    sType = CharField()
    HotelID = IntegerField()
