'''The basic user model (For logins)
The users will have roles i.e. chef, manager, host, waitress, etc..
'''
from peewee import CharField, IntegrityError, IntegerField, FloatField, CompositeKey, DateField
from asst.models import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class CreditCard(UserMixin, BaseModel):
    class Meta:
        db_table = 'CreditCard'
    '''A User model for who will be using the software. Users have different levels of access with different roles

    Current active roles:

        - customer
        - manager
    '''
    Cnumber = CharField()
    BillingAddr = CharField()
    Name = CharField()
    SecCode = CharField()
    Type = CharField()
    ExpDate = DateField()


    @classmethod
    def create_card(cls, cc, billaddr, name, csv, type, exp):
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
            cls.create(Cnumber = cc,
            BillingAddr = billaddr,
            Name = name,
            SecCode = csv,
            Type = type,
            ExpDate = exp)
        except IntegrityError:
            raise ValueError("User already exists")