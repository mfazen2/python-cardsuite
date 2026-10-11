# from tkinter import *
# from tkinter import ttk
import random
from time import sleep

class card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = None
        if rank > 10:
            if rank == 11:
                self.royal = "J"
                
            elif rank == 12:
                self.royal = 'Q'
            else:
                self.royal = "K"
            self.rank = rank
        else:
            self.royal = None
            self.rank = rank
        self.color = 'black' if suit in ['spades', 'clubs'] else 'red'

    def __repr__(self):
        return str(f"Suit: {self.suit}\nRank: {str(self.rank)}")
    def suitLetter(self):
        return self.suit[0].upper()
    def __str__(self):
        if self.rank == 10:
            return str(f"""
            __________
            |        |
            | {self.rank}     |
            |        |
            |   { self.suitLetter()}    |
            |        |
            |     {self.rank} |
            |________|
            """)
        elif self.rank > 10:
            return str(f"""
            __________
            |        |
            | {self.royal}      |
            |        |
            |   { self.suitLetter()}    |
            |        |
            |      {self.royal} |
            |________|
            """)
        else:    
            return str(f"""
            __________
            |        |
            | {self.rank}      |
            |        |
            |   { self.suitLetter()}    |
            |        |
            |      {self.rank} |
            |________|
            """)

class deck:
    def __init__(self,deckCount):
        self.deckCount= deckCount
        self.deckList=[]
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for _ in range(deckCount):
            for suit in suits:
                for i in range(1,14):
                    temp = card(suit,i)
                    self.deckList.append(temp)
        self.shuffle()
        print("Deck Created")

    def deal(self):
        if not self.deckList:
            return None
        r = random.randrange(len(self.deckList))
        card = self.deckList.pop(r)
        return card
        
    def shuffle(self):
        try:
            random.shuffle(self.deckList)
            return "Shuffled"
        except e:
            print(str(e))
            return None
    def __str__(self):
        out = ""
        for card in self.deckList:
            out += (str(card))
        return out


#for solitaire, create 7 arrays for the 7 stacks of cards, and restrict card placement if:
#the value is either 1. greater than the previous value, or 2. the same color

######## Solitaire ########


class SolitaireGameState:
    def __init__(self):
        self.deck = deck()

        #4 columns, all blank
        self.col1 = []
        self.col2 = []
        self.col3 = []
        self.col4 = []

    def gameStart(self):
        return None



######## (Simple) Blackjack ########

#blackjack is probably easier for now anyways

class BlackJackPlayer:
    def __init__(self):
        #much simpler since the player will choose everything, don't need behavior fields, unless we want to characterize a player's style --later
        self.name="Player"
        self.cards = []
        self.observedLarge=0
        self.observedSmall=0
        self.cardSum=0
        self.ace=0
        self.winLoss=0 #stand -> -1, win -> 1 -- will probably integrate multiple rounds/player stats later, good to have this field regardless
        
    def hitdecision(self):
        if self.cardSum == 0:
            return True
        elif self.cardSum >= 21:
            return False
        else:
            print(f"Your hand: {self.cardSum}")
            print(f"Observed Large Cards: {self.observedLarge}\nObserved Small Cards: {self.observedSmall}")
            decision = input("Do you want to hit or stand? If you stand, you cannot hit again & must wait until the end of the round. \nEnter your choice (Y/n): ").lower()
            return decision == "yes" or decision == "y"
        
    def react(self,myCard):
        self.cards.append(myCard)
        self.cardSum+=myCard.rank
        if (self.ace == 1 and (self.cardSum == 11)) or self.cardSum == 21:
            self.winLoss = 1
            print("Congratulations! You have won! Wait until the end of the round for your winnings.")
            sleep(1)
            print("Continuing round...")
            sleep(1)
        elif self.cardSum > 21:
            self.winLoss = -1
            print("Oh.. how tragic, it seems your luck ran out this round, good luck next time!")
            sleep(1)
            print("Continuing round...")
            sleep(1)
        else:
            self.winLoss = 0
    def observe(self,roundCards):
        for card in roundCards:
            if card.rank > 7: 
                self.observedLarge+=1
            else:
                self.observedSmall+=1
    def instantWin(self):
        instant_winCard = card("inswin",21)
        self.react(instant_winCard)
class BlackJackBot:
    def __init__(self, name,dealer):
        self.name = name
        self.cards=[]
        ### behavior fields ###
        self.dealer=dealer #we will use this to alternate between player & dealer hit/stand behavior
        #we will choose random values in a given range, and then use those values in another *random* choice machine

        self.confidence=random.randint(1,10)
        self.intelligence=random.randint(1,10)

        self.observedLarge=0
        self.observedSmall=0
        self.cardSum=0
        self.ace=0
        self.winLoss=0 #1 => win, #-1 => stand
    def hitdecision(self):
        if self.dealer:
            return (self.cardSum < 17)
        else:
            ### decision calculation ###
            
            result = 0.4 * (self.confidence / 10)
            result += 0.6 * (self.intelligence / 10) * (self.observedSmall/self.observedLarge) * (1 - (self.cardSum/21) - .2) if self.observedSmall > 0 and self.observedLarge > 0 else 7 * (self.intelligence / 10) * (1 - (self.cardSum/21) - .2)
            #use 0.3 * confidence to get our base decision
            #add 0.7 * intelligence * (observedSmall/observedLarge) * (1 - (cardSum/21) -.2) to get final
            return (result > 0.5)
    def react(self,myCard):
        if myCard.royal:
            self.cards.append(myCard)
            self.cardSum+=10
        else:
            self.cards.append(myCard)
            self.cardSum+=myCard.rank

        if (self.ace == 1 and (self.cardSum == 11)) or self.cardSum == 21:
            self.winLoss = 1
        elif self.cardSum > 21:
            self.winLoss = -1
        else:
            self.winLoss = 0
        
        ### react to current conditions ###
    def observe(self,roundCards):
        for card in roundCards:
            if card.rank > 7: 
                self.observedLarge+=1
            else:
                self.observedSmall+=1

### Gameplay Loop ###

#use the BlackJackBot class for automated tests

"""
Loop Design:
    The dealer will ask players if they wish to hit or hold, this result comes from the hitdecision method.

    So: 
        Loop over players -> call hitdecision (data is based on results of last hit)-> call react if hitdecision == TRUE
        If any player responds to react with a LOSS/STAND signal, remove them from the loop
        If any player responds to react with a WIN signal, continue the game
        Else continue
"""

class AutoBlackJack:
    def __init__(self):
        self.names = ['Max', 'Rosette', 'Lucy', 'Dealer']
        self.players=[]

        self.gameDeck = deck(4)

        for name in self.names:
            if name == "Dealer":
                self.players.append(BlackJackBot(name,True))
            else:
                self.players.append(BlackJackBot(name,False))

    def gameLoop(self):
        ### initial deal ###
        roundCards=[]
        for player in self.players:
            c1 = self.gameDeck.deal()
            c2 = self.gameDeck.deal()
            player.react(c1)
            player.react(c2)
            roundCards.append(c1)
            roundCards.append(c2)
            player.observe(roundCards)
        ### further deals ###
        roundCards=[]
        prev=None
        for player in self.players:
            if prev != None:
                player.observe(roundCards)
            while(player.hitdecision()):
                card = self.gameDeck.deal()
                player.react(card)
                roundCards.append(card)
                player.observe([card])
            if player.cardSum > 21:
                player.winLoss=-1
            

        ### review ###
        max = 0
        ties=[]
        winner = None
        for player in self.players:
            if player.cardSum > max and player.cardSum <= 21:
                winner = player.name
                max = player.cardSum
            print(f"Player {player.name} has a sum of {player.cardSum}.")
        for player in self.players:
            if player.cardSum == max:
                print(f"Player {winner} won with a sum of {max}!")

# print(f"Player {winner} won with a sum of {max}!")
# myGame = AutoBlackJack()
# myGame.gameLoop()

# myPlayer=BlackJackPlayer()
# print(myPlayer.hitdecision())
# myPlayer.instantWin()
#### Interactive Loop ####

class InteractiveBlackJack:
    def __init__(self):
        self.names = ['Player','Max', 'Rosette', 'Lucy', 'Dealer']
        random.shuffle(self.names)
        self.players=[]

        self.gameDeck = deck(4)

        for name in self.names:
            if name == "Dealer":
                self.players.append(BlackJackBot(name,True))    
            elif name == "Player":
                self.players.append(BlackJackPlayer())
            else:
                self.players.append(BlackJackBot(name,False))

    def gameLoop(self):
        ### initial deal ###
        roundCards=[]
        for player in self.players:
            c1 = self.gameDeck.deal()
            c2 = self.gameDeck.deal()
            player.react(c1)
            player.react(c2)
            roundCards.append(c1)
            roundCards.append(c2)
            player.observe(roundCards)
        ### further deals ###
        roundCards=[]
        prev=None
        for player in self.players:
            if prev != None:
                player.observe(roundCards)
            while(player.hitdecision()):
                card = self.gameDeck.deal()
                player.react(card)
                roundCards.append(card)
                player.observe([card])
            if player.cardSum > 21:
                player.winLoss=-1
            

        ### review ###
        max = 0
        ties=[]
        winner = None
        for player in self.players:
            if player.cardSum > max and player.cardSum <= 21:
                winner = player.name
                max = player.cardSum
            print(f"Player {player.name} has a sum of {player.cardSum}.")
        for player in self.players:
            if player.cardSum == max:
                print(f"Player {player.name} won with a sum of {max}!")


# myGame = InteractiveBlackJack()
# myGame.gameLoop()

myDeck = deck(1)
print(myDeck)