'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey, DateField, DecimalField
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Discount(UserMixin, BaseModel):
    class Meta:
        db_table = 'offer_room'
        primary_key = CompositeKey('Room_no', 'HotelID')
    '''A User model for who will be using the software. Users have different levels of access with different roles
    Current active roles:
        - customer
        - manager
    '''
    SDate = DateField()
    EDate = DateField()
    Discount = DecimalField()
    HotelID = IntegerField()
    Room_no = CharField()


    @classmethod
    def create_res(cls, sdate, edate, disc, hid, room_no):
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
                SDate = sdate,
                EDate = edate,
                Discount = disc,
                HotelID = hid,
                Room_no = room_no)
        except IntegrityError:
            raise ValueError("User already exists")