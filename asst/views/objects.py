import datetime
class Hotel:
    Country = 'America'#default america
    State= 'NJ'


class Room(Hotel):
    #manually add in service later Room.services = 'clean'
    rType='single' # single,double,deluxe,suite
    date1 = datetime.date.today()
    date2 = datetime.date(2018, 1, 14)
    eggs=0
    orangeJuice=0
    bacon=0





'''
x=tst1.date2-tst1.date1
y=x.days*2
'''



