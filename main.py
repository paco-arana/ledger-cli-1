from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY

my_table = PrettyTable()
my_table.field_names = ["Date", "Description", "Account", "Credit"]
my_table.align = "l"
my_table.align["Credit"] = "c"
my_table.set_style(MSWORD_FRIENDLY)
 
file1 = open("Bitcoin.ledger", "r")
lines = file1.readlines()

count = 1
hidden = 0
date = ""
desc = ""

def add_a_row(text_line):
    # Separate account from credit using the tabs (\t)
    new_line = text_line.split("\t")
    # Remove any empty strings from the line 
    new_line = list(filter(None, new_line))
    # Remove any breaks (\n) from the strings
    for i in range(len(new_line)):
        new_line[i] = new_line[i].replace('\n', '')
    # The element at index 0 is the account:    
    acc = new_line[0]
    # The element at index 1 is the credit:
    credit = new_line[1]

    my_table.add_row([date, desc, acc, credit])

for line in lines[1:]:

    if line.startswith("\t"):
        add_a_row(line)

    else:
        # Separate the string by spaces, isolate the first element
        new_line = line.split(" ", 1)
        # First element of the resulting list is the date 
        date = new_line[0]

        # Everything remaining is the description
        desc = new_line[1]
        desc = desc.replace("\n", "")



print(my_table)




