from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from django.http import JsonResponse
import json 
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

def service(request):
	if request.method == 'POST':
		json_data = json.loads(request.body.decode("utf-8"))
		board = json_data['grid']
		win = checkWin(board)	#user place X check if he already win
		if(win == 0 and isFull(board)):
			data = {
				'over': 1,
				'winner': ' ', 
				'grid': board
			}
			return JsonResponse(data)
		elif(win == 1):
			data = {
				'over': 1,
				'winner': 'X', 
				'grid': board
			}
			return JsonResponse(data)
		placeO(board)	#User not yet win, we make a move 	
		win = checkWin(board)
		if(win == 2):
			data = {
				'over': 1,
				'winner': 'O', 
				'grid': board
			}
			return JsonResponse(data)	
		elif(win == 0):
			data = {
				'over': 0,
				#'winner': ' ', 
				'grid': board
			}
			return JsonResponse(data)
		return 0
	else:
		return HttpResponse("ONLY ACCEPT POST INFORMATION")

def checkWin(board):
	#horizontal check X
	if(board[0] == 1 and board[1] == 1 and board[2] == 1):
		return 1
	if(board[3] == 1 and board[4] == 1 and board[5] == 1):
		return 1
	if(board[6] == 1 and board[7] == 1 and board[8] == 1):
		return 1
	#verticle check
	if(board[0] == 1 and board[3] == 1 and board[6] == 1):
		return 1
	if(board[1] == 1 and board[4] == 1 and board[7] == 1):
		return 1
	if(board[2] == 1 and board[5] == 1 and board[8] == 1):
		return 1
	#slash check
	if(board[0] == 1 and board[4] == 1 and board[8] == 1):
		return 1
	if(board[2] == 1 and board[4] == 1 and board[6] == 1):
		return 1
	#check O now
	#horizontal check O
	if(board[0] == 2 and board[1] == 2 and board[2] == 2):
		return 2
	if(board[3] == 2 and board[4] == 2 and board[5] == 2):
		return 2
	if(board[6] == 2 and board[7] == 2 and board[8] == 2):
		return 2
	#verticle check
	if(board[0] == 2 and board[3] == 2 and board[6] == 2):
		return 2
	if(board[1] == 2 and board[4] == 2 and board[7] == 2):
		return 2
	if(board[2] == 2 and board[5] == 2 and board[8] == 2):
		return 2
	#slash check
	if(board[0] == 2 and board[4] == 2 and board[8] == 2):
		return 2
	if(board[2] == 2 and board[4] == 2 and board[6] == 2):
		return 2
	return 0

def isFull(board):
	if(board[0] != 0 and board[1] != 0 and board[2] != 0 and
		board[3] != 0 and board[4] != 0 and board[5] != 0 and
		board[6] != 0 and board[7] != 0 and board[8] != 0):
		return True
	return False

def placeO(board):
	i = 0
	while i < len(board):
		if(board[i] == 0):
			board[i] = 2
			i = 10
		i += 1

def index2(request):
	return HttpResponse("Hello, world. You're at the polls index.")