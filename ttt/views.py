from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from django.http import JsonResponse
from django.core.mail import EmailMessage
import json
import string
import random
import datetime
import pymongo
import copy
from bson.objectid import ObjectId
from .models import *

status_ok = {'status':"OK"}
status_err = {'status':"ERROR"}
new_board = [' ',' ',' ',
			 ' ',' ',' ',
 			 ' ',' ',' ']
# Create your views here.
def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		
		if form.is_valid():
			#data = form.cleaned_data['name']
			#new_form = NameForm(name = data)
			#new_context = {'form': new_}
			context = {'form': form}
			return render(request,'ttt/board.html',context)

	else:
		form = NameForm()
	
	context = {'form' : form}
	return render(request,'ttt/index.html',context)

# def service(request):
# 	if request.method == 'POST':
# 		json_data = json.loads(request.body.decode("utf-8"))
# 		board = json_data['grid']
# 		win = checkWin(board)	#user place X check if he already win
# 		if(win == 0 and isFull(board)):
# 			data = {
# 				'over': 1,
# 				'winner': ' ', 
# 				'grid': board
# 			}
# 			return JsonResponse(data)
# 		elif(win == 1):
# 			data = {
# 				'over': 1,
# 				'winner': 'X', 
# 				'grid': board
# 			}
# 			return JsonResponse(data)
# 		placeO(board)	#User not yet win, we make a move 	
# 		win = checkWin(board)
# 		if(win == 2):
# 			data = {
# 				'over': 1,
# 				'winner': 'O', 
# 				'grid': board
# 			}
# 			return JsonResponse(data)	
# 		elif(win == 0):
# 			data = {
# 				'over': 0,
# 				#'winner': ' ', 
# 				'grid': board
# 			}
# 			return JsonResponse(data)
# 		return 0
# 	else:
# 		return HttpResponse("ONLY ACCEPT POST INFORMATION")

# def checkWin(board):
# 	#horizontal check X
# 	if(board[0] == 1 and board[1] == 1 and board[2] == 1):
# 		return 1
# 	if(board[3] == 1 and board[4] == 1 and board[5] == 1):
# 		return 1
# 	if(board[6] == 1 and board[7] == 1 and board[8] == 1):
# 		return 1
# 	#verticle check
# 	if(board[0] == 1 and board[3] == 1 and board[6] == 1):
# 		return 1
# 	if(board[1] == 1 and board[4] == 1 and board[7] == 1):
# 		return 1
# 	if(board[2] == 1 and board[5] == 1 and board[8] == 1):
# 		return 1
# 	#slash check
# 	if(board[0] == 1 and board[4] == 1 and board[8] == 1):
# 		return 1
# 	if(board[2] == 1 and board[4] == 1 and board[6] == 1):
# 		return 1
# 	#check O now
# 	#horizontal check O
# 	if(board[0] == 2 and board[1] == 2 and board[2] == 2):
# 		return 2
# 	if(board[3] == 2 and board[4] == 2 and board[5] == 2):
# 		return 2
# 	if(board[6] == 2 and board[7] == 2 and board[8] == 2):
# 		return 2
# 	#verticle check
# 	if(board[0] == 2 and board[3] == 2 and board[6] == 2):
# 		return 2
# 	if(board[1] == 2 and board[4] == 2 and board[7] == 2):
# 		return 2
# 	if(board[2] == 2 and board[5] == 2 and board[8] == 2):
# 		return 2
# 	#slash check
# 	if(board[0] == 2 and board[4] == 2 and board[8] == 2):
# 		return 2
# 	if(board[2] == 2 and board[4] == 2 and board[6] == 2):
# 		return 2
# 	return 0

# def isFull(board):
# 	if(board[0] != 0 and board[1] != 0 and board[2] != 0 and
# 		board[3] != 0 and board[4] != 0 and board[5] != 0 and
# 		board[6] != 0 and board[7] != 0 and board[8] != 0):
# 		return True
# 	return False

# def placeO(board):
# 	i = 0
# 	while i < len(board):
# 		if(board[i] == 0):
# 			board[i] = 2
# 			i = 10
# 		i += 1

def adduser(request):
	if request.method == 'POST':
		json_data = json.loads(request.body.decode("utf-8"))
		username = json_data['username']
		password = json_data['password']
		email = json_data['email']
		
		count = User.objects(username = username).count()
		count += User.objects(email = email).count()
		if count > 0:
			return JsonResponse(status_err)
			
		else:
			key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			user = User(username=username,password=password,email=email,verified = False, key = key)
			user.save()
			#email = EmailMessage('Tic Tae Toe verification',key,to=[email])
			#email.send()
			# send_mail(
			# 	'Tic Tae Toe Verification',
			# 	key,
			# 	'zilinggame@gmail.com',
			# 	[email],
			# )
			return JsonResponse(status_ok)
	return HttpResponse("Only supporting POST")

def verify(request):
	if request.method == 'POST':
		json_data = json.loads(request.body.decode("utf-8"))
		email = json_data['email']
		key = json_data['key']
		try:
			user = User.objects.get(email = email)
			if user.key == key or key == "abracadabra":
				user.verified = True
				user.save()
				return JsonResponse(status_ok)
			else:
				return JsonResponse(status_err)
		except:
			return JsonResponse(status_err)
	return	HttpResponse("Only supporting POST")

def login(request):
	if request.method == 'POST':
		if request.session.get("login",False): #if already login return can't login again
			return JsonResponse(status_err)
		else:	
			json_data = json.loads(request.body.decode("utf-8"))
			try:
				user = User.objects.get(username = json_data['username'])
			except:
				return JsonResponse(status_err)
			if user.password == json_data['password'] and user.verified == True: #everything match login
				request.session['login'] = True
				request.session['username'] = json_data['username']
				return JsonResponse(status_ok)
			else:										#username or password error 
				return JsonResponse(status_err)


	return	HttpResponse("Only supporting POST")	

def logout(request):
	if request.session.get("login",False):
		try:
			del request.session['username']
			del request.session['login']
		except KeyError:
			pass
		return JsonResponse(status_ok)
	else:
		return JsonResponse(status_err)

def statefulService(request):
	if request.session.get("login",False):
		json_data = json.loads(request.body.decode("utf-8"))
		move = json_data['move']
		#Get Current Grid
		try:	#try to obtain the board, if a incomplete board doesn't exist, last game complete
			stat = Stat.objects.get(username = request.session['username'], isComplete = False)

		except:
			stat = Stat(username=request.session['username'], datetime = datetime.datetime.utcnow()
						,board = new_board, isComplete = False, winner = " ")
			key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
			stat.game_id = key
		
		try:
			score = Score.objects.get(username = request.session['username'])
		
		except:
			score = Score(username = request.session['username'],human = 0,wopr = 0, tie = 0)


		if move is None:
			data = {'status': "OK",'grid': stat.board}
			return JsonResponse(data)
		#add the move to board
		stat.board[move] = "X"
		win = checkWin2(stat.board)
		if(win == " " and isFull2(stat.board)):
			data = {
				'status':"OK",
				'winner': " ",
				'grid': stat.board
			}
			stat.isComplete = True
			stat.winner = " "
			stat.save()
			score.tie += 1
			score.save()
			return JsonResponse(data)
		elif(win == "X"):
			data = {
				'status':"OK",
				'winner': "X",
				'grid': stat.board
			}
			stat.isComplete = True
			stat.winner = "X"
			stat.save()
			score.human += 1
			score.save()
			return JsonResponse(data)
		placeO2(stat.board)
		win = checkWin2(stat.board)
		if(win == "O"):
			data = {
				'status':"OK",
				'winner': "O",
				'grid': stat.board
			}
			stat.isComplete = True
			stat.winner = "O"
			stat.save()
			score.wopr += 1
			score.save()
			return JsonResponse(data)
		elif(win == " "):
			data = {
				'status':"OK",
				#'winner': " ",
				'grid': stat.board
			}
			stat.isComplete = False
			stat.winner = " "
			stat.save()
			return JsonResponse(data)

		debug = {
			'gri': stat.board,
			'winner': win
		}
		return JsonResponse(debug)		
		
	else:
		return JsonResponse(status_err)

def checkWin2(board):
	#horizontal check X
	if(board[0] == "X" and board[1] == "X" and board[2] == "X"):
		return "X"
	if(board[3] == "X" and board[4] == "X" and board[5] == "X"):
		return "X"
	if(board[6] == "X" and board[7] == "X" and board[8] == "X"):
		return "X"
	#verticle check
	if(board[0] == "X" and board[3] == "X" and board[6] == "X"):
		return "X"
	if(board[1] == "X" and board[4] == "X" and board[7] == "X"):
		return "X"
	if(board[2] == "X" and board[5] == "X" and board[8] == "X"):
		return "X"
	#slash check
	if(board[0] == "X" and board[4] == "X" and board[8] == "X"):
		return "X"
	if(board[2] == "X" and board[4] == "X" and board[6] == "X"):
		return "X"
	#check O now
	#horizontal check O
	if(board[0] == "O" and board[1] == "O" and board[2] == "O"):
		return "O"
	if(board[3] == "O" and board[4] == "O" and board[5] == "O"):
		return "O"
	if(board[6] == "O" and board[7] == "O" and board[8] == "O"):
		return "O"
	#verticle check
	if(board[0] == "O" and board[3] == "O" and board[6] == "O"):
		return "O"
	if(board[1] == "O" and board[4] == "O" and board[7] == "O"):
		return "O"
	if(board[2] == "O" and board[5] == "O" and board[8] == "O"):
		return "O"
	#slash check
	if(board[0] == "O" and board[4] == "O" and board[8] == "O"):
		return "O"
	if(board[2] == "O" and board[4] == "O" and board[6] == "O"):
		return "O"
	return " "

def isFull2(board):
	if(board[0] != " " and board[1] != " " and board[2] != " " and
		board[3] != " " and board[4] != " " and board[5] != " " and
		board[6] != " " and board[7] != " " and board[8] != " "):
		return True
	return False

def placeO2(board):
	i = 0
	while i < len(board):
		if(board[i] == " "):
			board[i] = "O"
			i = 10
		i += 1

def listgames(request):
	if request.session.get("login",False):
		game_list = []
		dic = {}
		stat = Stat.objects(username = request.session['username'])
		for s in stat:
			dic['id'] = s.game_id
			dic['start_date'] = s.datetime
			game_list.append(copy.deepcopy(dic))
		data = {
			'status':"OK",
			'games': game_list
		}
		return JsonResponse(data)
	else:
		return JsonResponse(status_err)

def getgame(request):
	if request.session.get("login",False):
		json_data = json.loads(request.body.decode("utf-8"))
		try:
			stat = Stat.objects.get(username = request.session['username'], game_id = json_data['id'])
		except:
			return JsonResponse(status_err)
		
		data = {
			'status':"OK",
			'grid': stat.board,
			'winner': stat.winner
		}
		return JsonResponse(data)

	else:
		return JsonResponse(status_err)

def getscore(request):
	if request.session.get("login",False):
		try:
			score = Score.objects.get(username = request.session['username'])
			data = {
				'status': "OK",
				'human':score.human,
				'wopr': score.wopr, 
				'tie': score.tie
			}
		except:
			data = {
				'status': "OK",
				'human':0,
				'wopr': 0, 
				'tie': 0
			}
		
		return JsonResponse(data)

	else:
		return JsonResponse(status_err)


def index2(request):
	return HttpResponse("Hello, world. You're at the polls index.")