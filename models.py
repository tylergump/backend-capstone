from peewee import *
import datetime

DATABASE = SqliteDatabase('goals.sqlite')

class Goal(Model):
    category = CharField()
    timeframe = CharField()
    wager = CharField()
    description = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Goal], safe=True)
    print("Tables Created")
    DATABASE.close()
    