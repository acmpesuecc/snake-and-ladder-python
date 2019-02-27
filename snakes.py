import termcolor as tc, random
import colorama
colorama.init()
def assign_color(players):
    """ assigns different colors to different player's beeds
        players: dictionary(name -> [beed,position])
        returns: dictionary(beed -> color)"""
    
    cl = ["red","green","cyan","magenta"]
    random.shuffle(cl)
    colors = {}
    counter = 0
    for m in players.keys():
        colors[players[m][0]] = cl[counter]
        counter += 1
    return colors

def prepare_board():
    """ make board in form of nested lists 
        returns: nested lists  """
 
    board = []
    temp = []
    for i in range(100,0,-1):
        temp.append(str(i))
        if (i-1)%10 == 0:
            board.append(temp)
            temp = []
    for j in range(len(board)):
        if j%2:
            board[j].reverse()
    return board

def display_board(players,board,colors):
    """ prints the board in a pretty manner
        players: dictionary(name -> [beed,position])
        board: list of numbers(use prepare_board() function
        returns: None
        """
    snakes_blocks = {16: 4, 33: 20, 48: 24, 62: 56, 78: 69, 94: 16,99: 9}
    ladder_blocks = {3: 12, 7: 23, 20: 56, 47: 53, 60: 72, 80: 94}
    
    # creates a dictionary (position -> (beed)) list is used due possibility of many beeds at a position
    beed_place = {}
    for i in players:
        if beed_place.get(players[i][1]):
            beed_place[players[i][1]].append(players[i][0])
        else:
            beed_place[players[i][1]] = list(players[i][0])
    
    print("".center(111,"-"))
    for i in board:
        print("|",end="")
        for j in i:
            if beed_place.get(int(j)):
                print(j.rjust(6),end="")
                for k in beed_place.get(int(j)):
                    print(tc.colored(k,colors[k],None,attrs=["bold"]),end="")
                print("".ljust(4-len(beed_place.get(int(j)))),end="")
            else:
                if snakes_blocks.get(int(j)):
                    print(j.rjust(6),end="")
                    print(tc.colored("∫","white",None,attrs=["blink","bold"]),end="")
                    print(" "*3,end= "")
                elif ladder_blocks.get(int(j)):
                    print(j.rjust(6),end="")
                    print(tc.colored("†","yellow",None,attrs=["blink","bold"]),end="")
                    print(" "*3,end= "")
                else:
                    print(j.center(10),end= "")
            print("|",end="")
        print()
        print("".center(111,"-"))   

def update_players(players,name,dice):
    """ updates the position of the the players
        players: dict(name -> [beed,number])
        dice: list
        returns: dict(name -> [beed,number]) """
    def is_snake(position):
        snakes_blocks = {16: 4, 33: 20, 48: 24, 62: 56, 78: 69, 94: 16, 99:9}
        if position in snakes_blocks:
            return (position,snakes_blocks[position])

    def is_ladder(position):
        ladder_blocks = {3: 12, 7: 23, 20: 56, 47: 53, 60: 72, 80: 94}
        if position in ladder_blocks:
            return (position,ladder_blocks[position])

    player_p = players[name][1]
    if is_snake(player_p + dice):
        print("A snake ∫ is found on \"%d\" and it bites you ..." %(is_snake(player_p + dice)[0]))
        print("Went to %d.\n" %(is_snake(player_p + dice)[1]))
        players[name][1] = is_snake(player_p + dice)[1]
    elif is_ladder(player_p + dice):
        print("WooW!! a ladder is found...\nClimb it fast...")
        print("Climbed up to \"%d\".\n" %(is_ladder(player_p + dice)[1]))
        players[name][1] = is_ladder(player_p + dice)[1]
    elif players[name][1] + dice < 101:
        players[name][1] += dice

def player_number(text):
    """ inputs the number of players by user and confirms it.
        text: str(what you want to print on the screen)
        returns: int """
    while True:
        try:
            temp = int(input(text))
            if temp < 5  and temp > 0:
                return temp
            elif temp > 4:
                print("Sorry!! we cant take more than 4 people.\n")
            elif temp < 1:
                print("I am afraid that's not possible !!\n")
        except ValueError:
            print("Enter a number please !!\n")

def list_players(numbers):
    """ makes dict of the players with beed and position 
        numbers: int
        returns: dict(name -> [beed,position]) """
    
    def check_player(players,text):
        """ takes player name and checks whether it's in it
            players: dict(name -> [beed,position])
            text: text you want to show to screen """
        while True:
            name = input(text).lower().strip()
            if name not in players:
                return name
            else:
                print("That player already exist please try to use abbreviation or another name..\n")

    players = {}
    ranking = ["first","second","third","fourth"]
    beeds = ["@","#","%","*"]
    random.shuffle(beeds)
    for i in range(numbers):
        temp_name = check_player(players,"Enter %s player's name: " %(ranking[i]))
        players[temp_name] = [beeds[i],1]
        print("Your beed is: %s :" %(tc.colored(beeds[i],"blue",None,["bold"])))
    return players

def random_chance(players):
    """ creates random chances of the players
        players: dict(name -> [beed,number])
        returns: """
    random_players = list(players.keys()).copy()
    random.shuffle(random_players)
    return random_players

def is_gameover(players):
    """ checks whether game is over or not 
        players: dict (name -> [beed,position])
        returns: Boolean """
    for i in players:
        if players[i][1] >= 100:
            return (False,i)
    return (True,"")

def dice(chance):
    print("".center(9,"_"))
    
    print("|",end="")
    if chance == 4 or chance == 6 or chance == 5:
        print(tc.colored("*   *".center(7),"yellow",None,attrs=["bold"]),end="")
    elif chance == 2:
        print(tc.colored("*".center(7),"yellow",None,attrs=["bold"]),end="")
    elif chance == 3:
        print(tc.colored("*".rjust(7),"yellow",None,attrs=["bold"]),end="")
    elif chance == 1:
        print("".rjust(7),end="")
    print("|")
    
    print("|",end="")
    if chance == 4 or chance == 6:
        print(tc.colored("*   *".center(7),"yellow",None,attrs=["bold"]),end="")
    elif chance == 3 or chance == 5:
        print(tc.colored("*".center(7),"yellow",None,attrs=["bold"]),end="")
    elif chance == 2 or chance == 1:
        print(tc.colored("*".center(7),"yellow",None,["bold"]),end="")
    print("|")

    if chance != 4 and chance != 2:
        print("|",end="")
        if chance == 5 or chance == 6:
            print(tc.colored("*   *".center(7),"yellow",None,attrs=["bold"]),end="")
        elif chance == 1:
            print("".center(7),end="")
        elif chance == 3:
            print(tc.colored("*".ljust(7),"yellow",None,attrs=["bold"]),end="")
        print("|")

    print("".center(9,"-"),"\n")

def play_game():
    
    print("\n"+"WELCOME TO".center(50,"."),"\n")
    print(r"""        /\		     |-----|
       //\\                  |-----|
       ||                    |-----|
       || SNAKES     and     |-----| LADDERS
       ||                    |-----|
    \\//                     |-----|
     \/	                     |-----|
    """)
    # ask user how many players (must be less than <=4)
    numbers = player_number("\nHow many people want to play:")
    # make dict of players
    players = list_players(numbers)
    # assign different color to the beads
    colors = assign_color(players) 
    # randomly assign the players chances
    random_chances = random_chance(players)
    # counter to keep track of the chances
    counter = 0
    # while all the player position <= 100
    while is_gameover(players)[0]:
        # show the board with the beeds
        display_board(players,prepare_board(),colors)
        # print whose chance is this and roll the dice
        crrnt_plyr = random_chances[counter%len(players)]
        # current player's beed
        crrnt_plyr_beed = players[crrnt_plyr][0]
        # colored beed of the current player
        crrnt_plyr_clr = tc.colored(crrnt_plyr_beed,colors[crrnt_plyr_beed],None,["bold"])
        if input("It's %s's %s chance:\nroll the DICE: " %(crrnt_plyr.capitalize(),crrnt_plyr_clr)).lower().strip() == "roll".lower().strip():
            current_chance = random.randrange(1,7)
            print("\nROLLING ...\n")
            print("It's a %s !." %(tc.colored(current_chance,"blue",None,["bold","underline"])))
            # show the dice image
            dice(current_chance)
            # see whose chance is this, roll the dice and move the player's beed
            update_players(players,crrnt_plyr,current_chance)
            if not(is_gameover(players)[0]):
                display_board(players,prepare_board(),colors)
        else:
            print("Your chance is dismissed because you did'nt roll the dice !!")
        # increase the counter
        counter += 1
    print("\n\nCONGO, %s is the winner\n\n" %(tc.colored(is_gameover(players)[1],"white",None,["bold","underline"])))                                                         
play_game()