import random
import csv
melds = []
temp = []
hearts = []
diamonds = []
spades = []
clubs = []
ai_choice = 0
ai_eval = False
singleplayer = False
multiplayer = False
suitlist = [hearts,diamonds,spades,clubs]
# Defining what a card is
class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit

  def show(self,i):
    print (i + 1,":",face[self.value - 1] , self.suit)

  def __lt__(self, other):
    return self.value < other.value
# variables present in the card class
suits = ["hearts♥", "diamonds♦", "spades♠", "clubs♣"]
values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
face = ["Ace of","2 of","3 of","4 of","5 of","6 of","7 of","8 of","9 of","10 of","Jack of","Queen of","King of"]
def drawcheck():
  if len(deck) == 0:
    print("the game is a draw")
    data = [deck_length,len(deck),turn,50,player1_score,player2_score,"draw"]
    with open('data.csv', 'a') as f:
      writer = csv.writer(f)
      writer.writerow(data)
    if simulation:
      game_start(True)
    else:
      game_start(False)
# Code for single player opponent
def computer_turn(playerdeck,playername,input,playerscore,singleplayer,multiplayer,player):
  global ai_eval
  global ai_choice
  global ans
  ai_eval = True
  ai_choice = 0
  createhormeld(input,playerscore,singleplayer,multiplayer,player)
  swap = random.randint(1,100)
  if swap >= 15:
    swap = 1
  else:
    swap = 2
  if swap == 1:
    discardpile.append(playerdeck[ans-1])
    playerdeck.remove(playerdeck[ans-1])
    playerdeck.append(discardpile[0])
    discardpile.remove(discardpile[0])
  if swap == 2:
    discardpile.append(playerdeck[ans-1])
    playerdeck.remove(playerdeck[ans-1])
    playerdeck.append(deck[0])
    deck.remove(deck[0])
    discardpile.remove(discardpile[0])
# Code for a players turn
def playerturn(playerdeck,playername):
  print("what would player",playername,"like to do 1 : Take from discard pile 2 : take from deck")
  ans = int(input())
  if ans == 1:
    print("what card would you like to swap with it :")
    ans = int(input())
    discardpile.append(playerdeck[ans-1])
    playerdeck.remove(playerdeck[ans-1])
    playerdeck.append(discardpile[0])
    discardpile.remove(discardpile[0])
  if ans == 2:
    print("what card would you like to swap with it :")
    ans = int(input())
    discardpile.append(playerdeck[ans-1])
    playerdeck.remove(playerdeck[ans-1])
    playerdeck.append(deck[0])
    deck.remove(deck[0])
    discardpile.remove(discardpile[0])
#checking for melds
def createhormeld(input,playerscore,singleplayer,multiplayer,player):
  #checks for repeated values, if a value is repeated more than three times the melds score is calculated and added to the players score
  playerscore = 0
  melds = []
  temp_cardlist = []
  for f in range (len(input)):
    temp_cardlist.append(input[f])
  for i in range (len(temp_cardlist)):
    melds.append(temp_cardlist[i].value)
  for l in range (1,14):
    if melds.count(l) >= 3:
      playerscore = playerscore + l*melds.count(l)
      for i in range (melds.count(l)):
        melded_values = (melds.index(l))
        temp_cardlist.remove(temp_cardlist[melded_values])
      break
  createvertmeld(temp_cardlist,playerscore,singleplayer,multiplayer,player,melds)
      
def checkascend(input,playerscore,singleplayer,multiplayer,player,melds):
  global player1_score, player2_score, ai_eval, ai_choice, ans, simulation
  for i in range (len(input)):
    for l in range (len(input[i])):
      if (input[i].count((input[i][l]) + 1)) >= 1 and (input[i].count(input[i][l] - 1)) >= 1:
        playerscore = playerscore + input[i][l] * 3
        if (input[i].count(input[i][l] + 2)) >= 1:
          playerscore = playerscore + (input[i][l] + 2)
          input[i].remove(input[i][l + 2])
          print(input[i][l])
          input[i].remove(input[i][l])
          input[i].remove(input[i][l])
          input[i].remove(input[i][l - 2])
          break
        else:
          input[i].remove(input[i][l])
          input[i].remove(input[i][l])
          input[i].remove(input[i][l - 2]) 
          break
  if ai_eval:
    ai_eval = False
    print(input)
    choice = []
    for i in range (len(input)):
      for l in range (len(input[i])):
        choice.append(input[i][l])
    print(choice)
    ans = melds.index(choice[random.randint(0,len(choice)-1)]) + 1
    print(ans)
  else:
    print("score :")
    print(playerscore)
    if player == ("player1"):
      player1_score = playerscore
    else:
      player2_score = playerscore
    if playerscore >= 50:
      global turn
      data = [deck_length,len(deck),turn,50,player1_score,player2_score,player]
      print("YOU WIN!!!!!!!!!!!!")
      with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
      if simulation:
        game_start(True)
      else:
        game_start(False)
    
def createvertmeld(input,playerscore,singleplayer,multiplayer,player,melds):
  hearts = []
  diamonds = []
  spades = []
  clubs = []
  suitlist = [hearts,diamonds,spades,clubs]
  for i in range (len(input)):
    if input[i].suit == ("hearts♥"):
      hearts.append(input[i].value)
    elif input[i].suit == ("diamonds♦"):
      diamonds.append(input[i].value)
    elif input[i].suit == ("spades♠"):
      spades.append(input[i].value)
    else:
      clubs.append(input[i].value)
  checkascend(suitlist,playerscore,singleplayer,multiplayer,player,melds)
#function to print out all the classes in a list
def showhand(input):
  for i in range (len(input)):
    input[i].show(i)
#function to update the cards in a players hand and then print relevant information
def updateDeck(player_deck_name,player_deck,player_score,singleplayer,multiplayer,player):
  global deck
  print("discard pile :")
  discardpile[0].show(0)
  print("")
  print(player_deck_name)
  showhand(player_deck)
  print("")
  createhormeld(player_deck,player_score,singleplayer,multiplayer,player)
#function for a turn in game
def runGame(player1,player2,discardpile,singleplayer,multiplayer):
  global turn, deck, simulation
  turn = turn + 1
  drawcheck()
  print("")
  print("Turn:",turn)
  print("---------")
  print("")
  updateDeck("player one's deck :",player1,player1_score,singleplayer,multiplayer,"player1")
  if simulation:
    computer_turn(player1,"player one",player1,player1_score,singleplayer,multiplayer,"player1")
  else:
    playerturn(player1,"player one")
  player1.sort()
  updateDeck("player one's deck :",player1,player1_score,singleplayer,multiplayer,"player1")
  drawcheck()
  updateDeck("player two's deck :",player2,player2_score,singleplayer,multiplayer,"player2")
  if multiplayer:
    playerturn(player2,"player two")
  else:
    computer_turn(player2,"player two",player2,player2_score,singleplayer,multiplayer,"player2")
  player2.sort()
  updateDeck("player two's deck :",player2,player2_score,singleplayer,multiplayer,"player2")
  # this was for the purpose of testing how the cards were moved: showhand(deck)
  runGame(player1,player2,discardpile,singleplayer,multiplayer)
#function for the initial menu that shows up
def game_start(recur):
  # Generating the deck
  global deck_length, simulation, player1_score, player2_score, discardpile, turn, deck
  deck = [Card(value, suit) for value in values for suit in suits]
  deck_length = (len(deck))
  random.shuffle(deck)
  print("NEW GAME")
  print("--------")
  # Generating the deck
  player1_score = 0
  player2_score = 0
  discardpile = []
  player1 = []
  player2 = []
  turn = 0
  deck = [Card(value, suit) for value in values for suit in suits]
  deck_length = (len(deck))
  random.shuffle(deck)
  #sorting the cards in the deck into the two hands the deck and the discard pile
  for i in range (10):
    player1.append(deck[i])
    deck.remove(deck[i])
  player1.sort()
  for i in range (10):
    player2.append(deck[i])
    deck.remove(deck[i])
  player2.sort()
  discardpile.append(deck[0])
  deck.remove(deck[0])
  if recur:
    singleplayer = False
    multiplayer = False
    runGame(player1,player2,discardpile,singleplayer,multiplayer)
  print("What would you like to play 1:Singleplayer 2:Multiplayer 3:Simulation")
  gamemode = input()
  singleplayer = False
  multiplayer = False
  simulation = False
  if gamemode == "1":
    singleplayer = True
    runGame(player1,player2,discardpile,singleplayer,multiplayer)
  elif gamemode == "2":
    multiplayer = True
    runGame(player1,player2,discardpile,singleplayer,multiplayer)
  elif gamemode == "3":
    simulation = True
    runGame(player1,player2,discardpile,singleplayer,multiplayer)
    
game_start(False)