'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, DecimalField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Room(UserMixin, BaseModel):
    class Meta:
        db_table = 'has_room'
        primary_key = CompositeKey('Room_no', 'HotelID')
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    Room_no = IntegerField()
    HotelID = IntegerField()
    Price = DecimalField(max_digits = 10, decimal_places = 2)
    Capacity = IntegerField()
    Floor_no = IntegerField()
    Description = CharField()
    Type = CharField() #assumption that user will enter valid role

    @classmethod
    def create_user(cls, room_no, hid, price, capacity, floor_no, desc, type):
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
    Room_no = room_no,
    HotelID = hid,
    Price = price,
    Capacity = capacity,
    Floor_no = floor_no,
    Description = desc,
    Type =type
)
        except IntegrityError:
            raise ValueError("User already exists")
