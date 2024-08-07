#THIS PROJECT WAS MADE TO SIMULATE A GAME OF MONOPOLY, WITH ABILITY TO SIMULATE FRoM ANY GAME POSITION
#!PRICES ARE IN MILIONS
import random,os,time
from time import sleep as wait
players=[

]
players_dict={

}
wins_loses={

}
draws=0
train_positions=[5,15,25,35]
energy_positions=[12,28]
HOUSESBOUGHT=0
HOTELSBOUGHT=0
TURNSGLOBAL=0
start_time=time.time()
class Player:
    def  __init__(self, money,name,owned_buildings=[]):
        self.money=money
        self.name=name
        self.owned_buildings=owned_buildings
        self.houses=0
        self.hotels=0
        self.jailcards=0
        self.current_position=0
        players.append(self)
        players_dict[self.name]=self
        self.wins=0
        self.loses=0
        self.inJail=False

class Building:
    def __init__(self,number,price,name,color,rent=[],sada=[],housePrice=0):
        self.number=number
        self.price=price
        self.name=name
        self.hotels=0
        self.houses=0
        self.color = color
        self.rent = rent#array of rent in format [basic, 1 house..., 4 houses, hotel]
        self.houses=0
        self.hasHotel=False
        self.sada=sada
        self.housePrice=housePrice

class Game:
    def __init__(self, numberOfPlayers,board):
        self.numberOfPlayers= numberOfPlayers
        self.board=board
board=[
    Building(0,0,'Start','special'),
    Building(1,0.6,'Klementska ulice','brown',[0.04, 0.6, 1.8, 3.2, 4.5],[1,3],1),
    Building(2,0,'Pokladna','special'),
    Building(3,0.6,'Revolucni ulice','brown',[0.04, 0.6, 1.8, 3.2, 4.5],[1,3],1),
    Building(4,0,'Dan z prijmu', 'special'),
    Building(5,2,'Wilsonovo nadrazi', 'train'),
    Building(6,1,'Panska ulice', 'light_blue',[0.08, 1.0, 3.0, 4.5, 6.0],[6,8,9],1),
    Building(7,0,'Sance','special' ),
    Building(8,1,'Jindriska ulice','light_blue',[0.08, 1.0, 3.0, 4.5, 6.0],[6,8,9],1),
    Building(9,1.2,'Vinohradska ulice','light_blue',[0.08, 1.0, 3.0, 4.5, 6.0],[6,8,9],1),
    Building(10,0,'Vezeni', "special"),
    Building(11,1.4,'Prvni ruzova', "pink",[0.1, 1.5, 4.5, 6.25, 7.5],[11,13,14],1),
    Building(12,2,'Elektrarna', "energy"),
    Building(13,1.4,'Druha ruzova', "pink",[0.1, 1.5, 4.5, 6.25, 7.5],[11,13,14],1),
    Building(14,1.6,'Treti ruzova', "pink",[0.1, 1.5, 4.5, 6.25, 7.5],[11,13,14],1),
    Building(15,2,'Holesovice nadrazi', "train"),
    Building(16,1.8,'Prvni oranzova', "orange",[0.12, 1.8, 5.0, 7.0, 9.0],[16,18,19],1),
    Building(17,0,'Sance', "special"),
    Building(18,1.8,'Druha oranzova', "orange",[0.12, 1.8, 5.0, 7.0, 9.0],[16,18,19],1),
    Building(19,2,'Treti oranzova', "orange",[0.12, 1.8, 5.0, 7.0, 9.0],[16,18,19],1),
    Building(20,0,'Parkovani', "special"),
    Building(21,2.2, "Strand", "Red", [0.14, 0.7, 2.0, 5.5, 7.5, 9.5]),
    Building(22,0,'Sance', "special"),
    Building(23,2.2, "Fleet Street", "Red", [0.14, 0.7, 2.0, 5.5, 7.5, 9.5]),
    Building(24,2.2, "Trafalgar Square", "Red", [0.14, 0.7, 2.0, 5.5, 7.5, 9.5]),
    Building(25,0,'Nadrazi 3', "train"),
    Building(26, 2.6,"Leicester Square", "Yellow", [0.16, 0.8, 2.2, 6.0, 8.0, 10.0]),
    Building(27, 2.6,"Coventry Street", "Yellow", [0.16, 0.8, 2.2, 6.0, 8.0, 10.0]),
    Building(28,2,'Vodarna', "energy"),
    Building(29, 2.6,"Piccadilly", "Yellow", [0.16, 0.8, 2.2, 6.0, 8.0, 10.0]),
    Building(30,0,'Go to jail', "special"),
    Building(31, 3,"Regent Street", "Green", [0.18, 0.9, 2.5, 7.0, 8.75, 10.5]),
    Building(32,0,'Pokladna', "special"),
    Building(33, 3,"Oxford Street", "Green", [0.18, 0.9, 2.5, 7.0, 8.75, 10.5]),
    Building(34, 3,"Bond Street", "Green", [0.18, 0.9, 2.5, 7.0, 8.75, 10.5]),
    Building(35,0,'Nadrazi 4', "train"),
    Building(36,0,'Sance', "special"),
    Building(38, 3.5,"Park Lane", "Dark Blue", [0.5, 2.5, 7.0, 17.5, 20.5, 23.0]),
    Building(39,-1,'Dan', "special"),
    Building(40, 3.5,"Mayfair", "Dark Blue", [0.5, 2.5, 7.0, 17.5, 20.5, 23.0])


]
'''
brown_rent = [0.04, 0.2, 0.6, 1.8, 3.2, 4.5]
light_blue_rent = [0.08, 0.4, 1.0, 3.0, 4.5, 6.0]
pink_rent = [0.1, 0.5, 1.5, 4.5, 6.25, 7.5]
orange_rent = [0.12, 0.6, 1.8, 5.0, 7.0, 9.0]

'''
def diceRoll(number_of_dices):
    total=0
    dice_rolls=[]
    previous_roll=0
    for i in range(number_of_dices):
        roll=random.randint(1,6)
        if previous_roll!=0:
            if previous_roll==roll:
                #print("rolling again")
                roll=random.randint(1,6)
            total+=roll
            dice_rolls.append(roll)
        else:
            previous_roll=roll
            total+=roll
            dice_rolls.append(roll)
    #?print(f"Rolled {total} in {number_of_dices} rolls.")
    return total
  
def drawBoard(board_arg):
    board=''
    for i in range(len(board_arg)):
        board+=("[")
        for player in players:
            if player.current_position==i:
                board+=player.name[0]

            else:
                board+='.'

        board+=("]")
    return board


hrac_1=Player(15,"kamil")
hrac_2=Player(15,"fofo")

owned_buildings=[]

games=0
turns=0
gamesNumber=1
for player in players:
    wins_loses[player.name]=0
def printBuildings(player):
    for i in player.owned_buildings:
        print(f"{board[i].name} | {board[i].price}")
gamesNumber=int(input('Number of games: '))
moves=1000
moves = int(input("How many turns till a draw: "))
setina=0
old_desetina = None
while True:
    if games!=0:
        setina = int((games/gamesNumber)*100)

    if not old_desetina == setina:
        os.system('cls')
        print(((setina)*'█')+(99-setina)*'▒')
        print(str(setina+1)+'%')
        old_desetina = setina
    
    
    for player in players:

        if player.inJail:
            roll1=diceRoll(1)
            roll2=diceRoll(1)
            if roll1!=roll2:
                continue
            else:
                player.inJail=False
        roll = diceRoll(2)
        #*Rolling dice
        if player.current_position+roll<len(board):
            player.current_position+=roll
            
        else:
            fuzzyPosition=player.current_position+roll - len(board)
            player.current_position=0
            player.current_position+=fuzzyPosition
            #print(f"{player.name} passed the start, got 2M")
            player.money+=2
        position=board[player.current_position]
        #*Buying things
        if player.money>=position.price and player.current_position not in owned_buildings and position.color!='special':
            player.money-=position.price
            player.owned_buildings.append(player.current_position)
            owned_buildings.append(player.current_position)
            #print(f"{player.name} bought {position.name}, money remaining {player.money}")
        if player.current_position in owned_buildings  and player.current_position not in player.owned_buildings:

            for i in players:
                
                if player.current_position in i.owned_buildings and position.houses==0:
                    if position.color=='special':
                        if position.name=='Go to jail':
                            player.current_position=10
                            if player.money>0.5:
                                player.inJail=False
                            else:
                                player.inJail=True
                    elif position.color=='train':
                        count=0
                        for build_id in train_positions:
                            if build_id in player.owned_buildings:
                                count+=1
                        player.money-=count*0.5
                        i.money+=count*0.5
                    elif position.color=='energy':
                        count=0
                        for build_id in energy_positions:
                            if build_id in player.owned_buildings:
                                count+=1
                        amount=0
                        if count==1:
                            amount=diceRoll(2)*0.04
                        elif count==2:
                            amount=diceRoll(2)*0.1
                        player.money-=amount
                        i.money+=amount
                                
                    elif not position.hasHotel:
                        player.money-=position.rent[position.houses]
                        i.money+=position.rent[position.houses]
                    elif position.hasHotel:
                        player.money-=position.rent[4]
                        i.money+=position.rent[4]

                    #print(f"{player.name} paid {position.price/2} for {position.name} to {i.name}")
        if player.current_position in player.owned_buildings and position.houses<=4:
            
            color = position.color
            maSadu=False
            for cislo_budovy in position.sada:
                if cislo_budovy not in player.owned_buildings:
                    maSadu=False
                    break
                else:
                    maSadu=True
            if maSadu and position.houses==4 and player.money>position.housePrice:
                player.money-=position.housePrice
                position.houses=0
                position.hasHotel=True
                HOTELSBOUGHT+=1
            elif maSadu and player.money>position.housePrice:
                player.money-=position.housePrice
                position.houses+=1
                HOUSESBOUGHT+=1
        



                    
    turns+=1 
    TURNSGLOBAL+=1  

    if turns>moves:
        draws+=1
        games+=1


        turns=0
        owned_buildings=[]
        players=[

        ]
        players_dict={

        }
        hrac_1=Player(15,"kamil")
        hrac_2=Player(15,"fofo")
    #print(drawBoard(board))
    for player in players:
        #print(f"{player.name} has {player.money} M")
        if player.money<0 :

            #print(f"Player {player.name} has lost!!!")
            #printBuildings(player)
            player.loses+=1
            
            for i in players:
                if i.name!=player.name:
                    i.wins+=1
                    wins_loses[i.name]+=1


            games+=1

            turns=0
            owned_buildings=[]
            players=[

            ]
            players_dict={

            }
            hrac_1=Player(15,"kamil")
            hrac_2=Player(15,"fofo")
    
     
    if games>=gamesNumber:
        print(f'simulated {games} games')
        end_time=time.time()
        with open("results.txt",'a') as f:
            for player in wins_loses:
                f.write(str(player)+'|'+str(wins_loses[player])+'\n')
            f.write("\ndraws"+str(draws))

            f.write(f"\n Draw is defined as a game that lasted more than {moves} moves.\n {HOUSESBOUGHT} houses were bought\n {HOTELSBOUGHT} hotels were bought\n If each turn took a minute on average, this simulation would have taken {round(TURNSGLOBAL*gamesNumber/60)} hours, the simulation took {round((end_time-start_time)/60,2)} minutes")
        print("Check results in results.txt")
        wait(1000)

    #continue_=input("press enter to continue")

    
