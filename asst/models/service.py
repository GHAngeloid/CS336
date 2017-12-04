'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Service(UserMixin, BaseModel):
    class Meta:
        db_table = 'Provides_Service'
        primary_key = CompositeKey('sType', 'HotelID')
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    sCost = IntegerField()
    sType = CharField()
    HotelID = IntegerField()


    @classmethod
    def create_user(cls, sCost, sType, hotelid):
        '''Creates a new user

        Args:
            email(str): The user email
            password(str): The password string - no need to hash beforehand
            name(str): name, doesn't have to be unique
            address(str): address of the user
            phone_no(str): phone number of the user
            role(str): The user role. admin, manager, chef, host, etc..

        Returns:
            N/A

        Raises:
            ValueError: When cid already exists
        '''

        try:
            cls.create(
                sCost = sCost,
                sType = sType,
                HotelID = hotelid)
        except IntegrityError:
            raise ValueError("User already exists")
