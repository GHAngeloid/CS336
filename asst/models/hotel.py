'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Hotel(UserMixin, BaseModel):
    class Meta:
        db_table = 'Hotel'
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    HotelID = IntegerField(primary_key=True)
    Street = CharField(unique = True)
    City = CharField()
    State = CharField()
    Country = CharField()
    Zip = CharField()

    @classmethod
    def create_hotel(cls, hotelid, street, city, state, country, zip):
        '''Creates a new hotel


        Returns:
            N/A

        Raises:
            ValueError: When cid already exists
        '''

        try:
            cls.create(
                HotelID = hotelid,
                street = street,
                city = city,
                state = state,
                country = country,
                zip = zip)
        except IntegrityError:
            raise ValueError("Hotel already exists")
