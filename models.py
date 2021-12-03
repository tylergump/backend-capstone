from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('goals.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Goal(Model):
    category = CharField()
    timeframe = CharField()
    wager = CharField()
    description = ForeignKeyField(User, backref="goals")
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Goal], safe=True)
    print("Tables Created")
    DATABASE.close()
    