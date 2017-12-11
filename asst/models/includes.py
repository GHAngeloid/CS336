'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Inc_Breakfast(UserMixin, BaseModel):
    class Meta:
        db_table = 'includes_breakfast'
        primary_key = CompositeKey('BType', 'InvoiceNo', 'HotelID')

    BType = CharField()
    InvoiceNo = IntegerField()
    HotelID = IntegerField()


    @classmethod
    def create_i_b(cls, btype, inv_no, hotelid):


        try:
            cls.create(
                InvoiceNo = inv_no,
                BType = btype,
                HotelID = hotelid)
        except IntegrityError:
            raise ValueError("Entry already exists")

class Cont_Service(UserMixin, BaseModel):
    class Meta:
        db_table = 'contains_service'
        primary_key = CompositeKey('sType', 'InvoiceNo', 'HotelID')

    sType = CharField()
    InvoiceNo = IntegerField()
    HotelID = IntegerField()


    @classmethod
    def create_c_s(cls, stype, inv_no, hotelid):


        try:
            cls.create(
                InvoiceNo = inv_no,
                sType = stype,
                HotelID = hotelid)
        except IntegrityError:
            raise ValueError("Entry already exists")