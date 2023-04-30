from prettytable import PrettyTable
import re

my_table = PrettyTable()
my_table.field_names = ["Date", "Description", "Account"]
my_table.align = "l"
 
file1 = open("Bitcoin.ledger", "r")
lines = file1.readlines()

count = 1
hidden = 0
date = ""
desc = ""
for line in lines[1:]:
    if count == 1:
        # Separate the string by spaces, isolate the first element
        new_line = line.split(" ", 1)
        # First element of the resulting list is the date 
        date = new_line[0]

        # Everything remaining is the description
        desc = new_line[1]
        desc = desc.replace("\n", "")

        # These two lines were moved down
        # my_table.add_column("Date", [date, date])
        # my_table.add_column("Description", [desc, desc])
        count += 1
    
    elif count == 2:
        # Explode the line
        print(str(line))
        new_line = line.split("\t")
        print(new_line)
        acc = new_line[1]
        print(acc)
        my_table.add_row([date, desc, acc])
        # my_table.field_names = ["Account"]
        # my_table.add_row(acc)
        # print(acc)
        count += 1
    else:
        # Explode the line
        print(str(line))
        new_line = line.split("\t")
        print(new_line)
        acc = new_line[1]
        print(acc)
        my_table.add_row([date, desc, acc])
        # my_table.field_names = ["Account"]
        # my_table.add_row(acc)
        # print(acc)
        count = 1

print(my_table)

