from django.db import models
from mongoengine import *
	  
connect('warmup')
# Create your models here. DateTimeField(),datetime.datetime.now
class User(Document):	#collection name user
	username = StringField()
	password = StringField()
	email = StringField()
	verified = BooleanField()
	key = StringField()

class Score(Document):
	username = StringField()
	human = IntField()
	wopr = IntField()
	tie = IntField()
 
class Stat(Document):
	username = StringField()
	game_id = StringField()
	datetime = DateTimeField()
	winner = StringField()
	board = ListField()
	isComplete = BooleanField()

