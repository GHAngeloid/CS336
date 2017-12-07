'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey, DateField
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Reservation(UserMixin, BaseModel):
    class Meta:
        db_table = 'Reservation'
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    InvoiceNo = IntegerField(primary_key=True)
    ResDate = DateField()
    OutDate = DateField()
    InDate = DateField()
    Room_no = IntegerField()
    HotelID = IntegerField()
    CNumber = CharField()
    CID = IntegerField()
    TotalAmt = FloatField()  #new field to account for partial key 'TotalAmt'


    @classmethod
    def create_res(cls, res_date, out_date, in_date, room_no, hid, cnum, cid):
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
                ResDate = res_date,
                OutDate = out_date,
                InDate = in_date,
                Room_no = room_no,
                HotelID = hid,
                CNumber = cnum,
                CID = cid)
        except IntegrityError:
            raise ValueError("User already exists")
