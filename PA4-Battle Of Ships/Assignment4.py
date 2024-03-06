import sys

# It is for the ship finder. If there is no ship in the checked square, it will give this error.
class ShipError(Exception):
    pass

# It is the error type that used for errors other than specified errors.
class GenericError(Exception):
    pass

def create_board(file):
    board = list()
    # It opens the file, splits it into lines and, saves into a list.
    with open(file) as f:
        line_list = f.read().split("\n")
    for line in line_list:
    # For each line, it creates the row and saves into the list.
        row = list()
        squares = line.split(";")
        for square in squares:
            if(square=="C" or square=="B" or square=="D" or square=="S" or square=="P"):
                row.append(square)
            elif(square==""):
                row.append("-")
            # It throws an error if there is a character other than expected.
            else:
                raise GenericError
        assert len(row) == 10
        board.append(row)
    assert len(board) == 10
    return board

def read_in_files(file):
    # It opens the file, splits each command and, saves all lines except the last blank line as a list.
    with open(file) as f:
        data = f.read().split(";")[:-1]
    return data

def write_output(file, output):
    with open(file, "w") as f:
        f.write(output)

def default_ship_counts(ship_type):
    if(ship_type=="C" or ship_type=="D" or ship_type=="S"):
        return 1
    elif(ship_type=="B"):
        return 2
    elif(ship_type=="P"):
        return 4

def find_ship_length(ship_type):
    if(ship_type=="C"):
        return 5
    elif(ship_type=="B"):
        return 4
    elif(ship_type=="D" or ship_type=="S"):
        return 3
    elif(ship_type=="P"):
        return 2

def find_ships(board):
    # Returns a dict that stores dicts whose keys are ship types and which hold the ship's properties.
    ships = {"C":dict(), "B":dict(), "D":dict(), "S":dict(), "P":dict()}
    # It stores column numbers where ships are found. 
    # Each number's count represents how many rows later that column will be empty.
    ship_positions = list()
    for i in range(len(board)):
        j = 0
        while j<len(board[i]):
            # It checks if there is currently a ship in that square.
            if(j not in ship_positions):
                if(board[i][j]!="-"):
                    ship_length = find_ship_length(board[i][j])
                    ship_count = len(ships[board[i][j]])
                    # This try block checks if there is a horizontally positioned ship.
                    try:
                        for k in range(j + 1, j + ship_length):
                            if(board[i][k]!=board[i][j]):
                                raise ShipError
                        ships[board[i][j]][ship_count]= [[i], list(range(j, j + ship_length)), ship_length]
                        # It passes the founded ship.
                        j += ship_length - 1
                    # If not, another try block checks for a vertically positioned ship.
                    except:
                        try:
                            for k in range(i + 1, i + ship_length):
                                if(board[k][j]!=board[i][j]):
                                    raise ShipError
                            ships[board[i][j]][ship_count] = [list(range(i, i + ship_length)), [j], ship_length]
                    # It adds as many column numbers as it indicates how many rows this column will be bypassed.
                            for l in range(ship_length):
                                ship_positions.append(j)
                        except:
                            pass
            j += 1
        # It removes one of each different number before going on each new row.
        for number in range(len(board)):
            try:
                ship_positions.remove(number)
            except:
                pass
    for ship_type in ships:
        assert len(ships[ship_type]) == default_ship_counts(ship_type)
    return ships

def did_it_sink(ships, ship_type, health, ship):
    # It checks if the ship has sunk and if it has sunk it deletes the ship from the dict.
    if(health==0):
        ships[ship_type].pop(ship)
    # If there are no ships of that type left, it deletes that type from the dictionary.
    if(len(ships[ship_type])==0):
        ships.pop(ship_type)

def play(board, ships, coordinates):
    r = int(coordinates[0]) - 1
    c = alphabet.index(coordinates[1])
    assert 0<=r<10 and c<10
    square = board[r][c]
    if(square=="-"):
        board[r][c] = "O"
    elif(square=="O" or square=="X"):
        None
    else:
        board[r][c] = "X"
        try:
            # It finds which ship the hit ship is and reduces its health by one.
            for ship in ships[square]:
                for horizontal in ships[square][ship][0]:
                    if(horizontal==r):
                        for vertical in ships[square][ship][1]:
                            if(vertical==c):
                                ships[square][ship][2] -= 1
                                did_it_sink(ships, square, ships[square][ship][2], ship)
                                # Error given to exit the loop.
                                raise RuntimeError
        # Exception for when the ship is found and gives a runtime error.
        except RuntimeError:
            pass

# Function used to create rows of hidden tables' of players'.
def create_row(board, i):
    row = "{:<2,d}".format(i + 1)
    for j in range(len(board[i])):
        if(board[i][j]=="O" or board[i][j]=="X"):
            row += "{} ".format(board[i][j])
        else:
            row += "{} ".format("-")
    row.rstrip()
    return row

# Function used to create hidden tables of players'.
def create_table(board1, board2):
    table = "Player1's Hidden Board\t\tPlayer2's Hidden Board\n  A B C D E F G H I J\t\t  A B C D E F G H I J\n"
    for i in range(len(board1)):
        table += create_row(board1, i) + "\t\t" + create_row(board2, i) + "\n"
    return table + "\n"

# Function that finds the number of remaining ships.
def ship_counter(ships, ship_type):
    try:
        return len(ships[ship_type])
    except KeyError:
        return 0

# Function that creates the ship's chart.
def ship_chart(ships, ship_type):
    ship_count = ship_counter(ships, ship_type)
    default_ship_count = default_ship_counts(ship_type)
    return ((default_ship_count - ship_count) * "X " + ship_count * "- ").rstrip()

# Function that creates the ship table.
def create_ship_table(ships1, ships2):
    c1 = ship_chart(ships1, "C")
    b1 = ship_chart(ships1, "B")
    d1 = ship_chart(ships1, "D")
    s1 = ship_chart(ships1, "S")
    p1 = ship_chart(ships1, "P")
    c2 = ship_chart(ships2, "C")
    b2 = ship_chart(ships2, "B")
    d2 = ship_chart(ships2, "D")
    s2 = ship_chart(ships2, "S")
    p2 = ship_chart(ships2, "P")
    table = """Carrier\t\t{}\t\t\t\tCarrier\t\t{}\nBattleship\t{}\t\t\t\tBattleship\t{}
Destroyer\t{}\t\t\t\tDestroyer\t{}\nSubmarine\t{}\t\t\t\tSubmarine\t{}
Patrol Boat\t{}\t\t\tPatrol Boat\t{}""".format(c1, c2, b1, b2, d1, d2, s1, s2, p1, p2)
    return table

# Function that creates the table of each round.
def create_output(board1, board2, ships1, ships2):
    table = create_table(board1, board2)
    ship_table = create_ship_table(ships1, ships2)
    return table + ship_table

try:
    output = ""

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    board1 = create_board(sys.argv[1])
    board2 = create_board(sys.argv[2])

    input1 = read_in_files(sys.argv[3])
    input2 = read_in_files(sys.argv[4])

    ships1 = find_ships(board1)
    ships2 = find_ships(board2)

    base_table = create_output(board1, board2, ships1, ships2)

    base_intro = "Player1's Move\n\nRound : 1\t\t\t\t\tGrid Size: 10x10\n\n"

    output += "Battle of Ships Game\n\n" + base_intro + base_table + "\n\n"

    player1_counter = 0
    player2_counter = 0
    round_counter = 1
    turn = 1
    # It shows who the winner is. It is 1 for player1, -1 for player2, 0 for draw.
    win = 0

    while True:
        if(turn==1):
            # If an error occurs in one of the turns, it uses if statements to identify the cause of the error and append it to the output.
            # If an error occurs, it stays in the same round until it is played without error.
            command = input1[player1_counter]
            try:
                coordinates = command.split(",")
                output += "Enter your move: {}\n".format(command)
                play(board2, ships2, coordinates)
                table = create_output(board1, board2, ships1, ships2)
                intro = "\nPlayer{:d}'s Move\n\nRound : {:d}\t\t\t\t\tGrid Size: 10x10\n\n".format(2, round_counter)
                output += intro + table + "\n\n"
                turn = 2
                if(len(ships2)==0):
                    win += 1
            except IndexError:
                if(len(coordinates)==1):
                    if(coordinates[0]==""):
                        message = "This command doesn't have any arguments"
                    else:
                        message = "This command has just one argument"
                else:
                    if(coordinates[0]==""):
                        if(coordinates[1]==""):
                            message = "This command's arguments are empty"
                        else:
                            message = "This command's first argument is empty"
                    else:
                        message = "This command's second argument is empty"
                output += "IndexError: {}.\n".format(message)
                round_counter -= 1
            except ValueError:
                try:
                    int(coordinates[0])
                except:
                    try:
                        alphabet.index(coordinates[1])
                    except:
                        message = "First argument is a non-numeric value and second argument isn't a letter"
                    else:
                        message = "First argument is a non-numeric value"
                else:
                    try:
                        alphabet.index(coordinates[1])
                    except:
                        message = "Second argument isn't a letter"
                output += "ValueError: {}.\n".format(message)
                round_counter -= 1
            except AssertionError:
                output += "AssertionError: Invalid Operation.\n"
                round_counter -= 1
            finally:
                player1_counter += 1
        if(turn==2):
            command = input2[player2_counter]
            try:
                coordinates = command.split(",")
                output += "Enter your move: {}\n".format(command)
                play(board1, ships1, coordinates)
                table = create_output(board1, board2, ships1, ships2)
                if(len(ships1)==0):
                    win -= 1
                    break
                intro = "\nPlayer{:d}'s Move\n\nRound : {:d}\t\t\t\t\tGrid Size: 10x10\n\n".format(1, round_counter + 1)
                output += intro + table + "\n\n"
                turn = 1
            except IndexError:
                if(len(coordinates)==1):
                    if(coordinates[0]==""):
                        message = "This command doesn't have any arguments"
                    else:
                        message = "This command has just one argument"
                else:
                    if(coordinates[0]==""):
                        if(coordinates[1]==""):
                            message = "This command's arguments are empty"
                        else:
                            message = "This command's first argument is empty"
                    else:
                        message = "This command's second argument is empty"
                output += "IndexError: {}.\n".format(message)
                round_counter -= 1
            except ValueError:
                try:
                    int(coordinates[0])
                except:
                    try:
                        alphabet.index(coordinates[1])
                    except:
                        message = "First argument is a non-numeric value and second argument isn't a letter"
                    else:
                        message = "First argument is a non-numeric value"
                else:
                    try:
                        alphabet.index(coordinates[1])
                    except:
                        message = "Second argument isn't a letter"
                output += "ValueError: {}.\n".format(message)
                round_counter -= 1
            except AssertionError:
                output += "AssertionError: Invalid Operation.\n"
                round_counter -= 1
            finally:
                player2_counter += 1
        round_counter += 1

    if(win==1):
        winner = "Player1 Wins!"
    elif(win==-1):
        winner = "Player2 Wins!"
    else:
        winner = "Player1 Wins!, Player2 Wins!, It is a Draw!"
    
    final = "\n{}\n\nFinal Information\n\n{}".format(winner, table)
    output += final
except IOError:
    correct_inputs = ["Assignment4.py", "Player1.txt", "Player2.txt", "Player1.in", "Player2.in"]
    incorrect_inputs = [correct_inputs[i] for i in range(1,5) if sys.argv[i]!=correct_inputs[i]]
    output += "IOError: input file(s) {} is/are not reachable.".format(", ".join(incorrect_inputs))
except:
    output += "kaBOOM: run for your life!"

write_output("Battleship.out", output)
print(output)

# Name: Ahmet İkbal
# Surname: Kayapınar
# Number: 2210356043