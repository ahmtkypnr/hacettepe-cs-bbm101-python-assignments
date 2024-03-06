import sys

stadium = dict()
# Output is a list so, every command appends their own output to main output variable
output = list()

def create_cat(cat_name, row, column):
    # Checks if the category exists
    if(cat_name not in stadium):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cat = dict()
        # Categories are keys of stadium dictionary and theirare values dictionaries
        # For loops creating nested dictionaries
        for i in range(row):
            # The keys of each category dictionary are rows and its values are dictionaries
            cat[alphabet[i]] = dict()
            for j in range(column):
                # Also, the keys of each row dictionary are columns and its values represents each seat
                cat[alphabet[i]][j] = "X"
        stadium[cat_name] = cat
        return "The category '{}' having {} seats has been created".format(cat_name, row * column)
    else:
        return "Warning: Cannot create the category for the second time. The stadium has already {}.".format(cat_name)
    
def sell(name, ticket_type, cat_name, seats):
    cat = stadium[cat_name]
    # If there are more than one seat it splits they by using for loop
    for seat in seats:
        # Splits seat's column number and row letter
        r = seat[0]
        # Checks if the row exists in the category
        if(r in cat):
            c = seat[1:]
            # Splits the beginning and the end of the range if seat range is given
            if("-" in c):
                cs = c.split("-")
                first = int(cs[0])
                last = int(cs[1])
                # Checks if the last column number given exceeds the number of columns in the category
                if(last<len(cat[r])):
                    empty = True
                    # Checks if each seat is empty
                    for i in range(first, last + 1):
                        if(cat[r][i]!="X"):
                            empty = False
                    # Checks ticket type and sells the ticket
                    if(empty==True):
                        for i in range(first, last + 1):
                            if(ticket_type=="student"):
                                cat[r][i] = "S"
                            elif(ticket_type=="full"):
                                cat[r][i] = "F"
                            elif(ticket_type=="season"):
                                cat[r][i] = "T"
                        output.append("Success: {} has bought {} at {}".format(name, seat, cat_name))
                    else:
                        output.append("Error: The seats {} cannot be sold to {} due some of them have already been sold!".format(seat, name))
                else:
                    output.append("Error: The category '{}' has less column than the specified index {}!".format(cat_name, seat))
            else:
                # If seat range isn't given it just checks seat availability and sells the ticket
                c = int(c)
                if(c in cat[r]):
                    if(cat[r][c]=="X"):
                        if(ticket_type=="student"):
                            cat[r][c] = "S"
                            output.append("Success: {} has bought {} at {}".format(name, seat, cat_name))
                        elif(ticket_type=="full"):
                            cat[r][c] = "F"
                            output.append("Success: {} has bought {} at {}".format(name, seat, cat_name))
                        elif(ticket_type=="season"):
                            cat[r][c] = "T"
                            output.append("Success: {} has bought {} at {}".format(name, seat, cat_name))
                    else:
                        output.append("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat, name))
                else:
                    output.append("Error: The category '{}' has less column than the specified index {}!".format(cat_name, seat))
        else:
            output.append("Error: The category '{}' has less row than the specified index {}!".format(cat_name, seat))

def cancel(cat_name, seats):
        cat = stadium[cat_name]
        # If there are more than one seat it splits they by using for loop
        for seat in seats:
            # Splits seat's column number and row letter
            r = seat[0]
            c = int(seat[1:])
            # Checks if the row exists in the category
            if(r in cat):
                # Checks if the last column number given exceeds the number of columns in the category
                if(c in cat[r]):
                    # Checks if each seat has been sold
                    if(cat[r][c]!="X"):
                        cat[r][c] = "X"
                        output.append("Success: The seat {} at '{}' has been canceled and now ready to sell again".format(seat, cat_name))
                    else:
                        output.append("Error: The seat {} at '{}' has already been free! Nothing to cancel".format(seat, cat_name))
                else:
                    output.append("Error: The category '{}' has less column than the specified index {}!".format(cat_name, seat))
            else:
                output.append("Error: The category '{}' has less row than the specified index {}!".format(cat_name, seat))

def balance(cat_name):
    out = "Category report of '{}'\n{}\n".format(cat_name, "-" * (21 + len(cat_name)))
    cat = stadium[cat_name]
    student, full, season = 0, 0, 0
    # By using for loops it checks every seat's ticket type
    for r in cat:
        for c in cat[r]:
            # It is like a counter so, it increases the correct ticket type's variable if the seat was sold
            if(cat[r][c]=="S"):
                student += 1
            elif(cat[r][c]=="F"):
                full += 1
            elif(cat[r][c]=="T"):
                season += 1
    revenue = student * 10 + full * 20 + season * 250
    out += "Sum of students = {}, Sum of full pay = {}, Sum of season ticket = {}, and Revenues = {} Dollars".format(student, full, season, revenue)
    return out
    
def show(cat_name):
    cat = stadium[cat_name]
    # It uses list instead of string for faster execution
    table = list()
    line = ""
    # It adds column line to the table
    for i in cat["A"]:
        line += "{:>3}".format(i)
    table.append(line)
    for r in cat:
        # It adds each row's name to the begining
        line = ""
        line += "{:<2}".format(r)
        for c in cat[r]:
            # It adds each seat's situation
            line += "{:<3}".format(cat[r][c])
        # Deletes the excess spaces
        line = line.rstrip()
        table.append(line)
    table.append("Printing category layout of {}".format(cat_name))
    # Reverses the list because the for loop adds them in alphabetical order
    table.reverse()
    table = "\n".join(table)
    return table

# Reads all file and saves into data variable
with open(sys.argv[1]) as file: 
    data = file.read()
line_list = data.split("\n")

# Splits data into lines
for line in line_list:
    # Splits commands and arguments using the space between them
    com, arg = line.split(" ", maxsplit=1)
    # Each if statement checks if the command is the one they contain
    # For commands with more than one argument, it also splits them
    if(com=="CREATECATEGORY"):
        cat_name, size = arg.split(" ")
        row, column = size.split("x")
        output.append(create_cat(cat_name, int(row), int(column)))
    elif(com=="SELLTICKET"):
        name, ticket_type, cat_name, seat = arg.split(" ", maxsplit=3) 
        seats = seat.split(" ")
        sell(name, ticket_type, cat_name, seats)
    elif(com=="CANCELTICKET"):
        cat_name, seat = arg.split(" ", maxsplit=1)
        seats = seat.split(" ")
        cancel(cat_name, seats)
    elif(com=="BALANCE"):
        output.append(balance(arg))
    elif(com=="SHOWCATEGORY"):
        output.append(show(arg))

# Converts output list to a string and adds a new line between each statement
output = "\n".join(output)

with open("output.txt", "w") as file:
    file.write(output)

print(output)

# Name: Ahmet İkbal
# Surname: Kayapınar
# Number: 2210356043