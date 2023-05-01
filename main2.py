from entry_maker import entry_maker
from tabulate import tabulate
import pandas as pd

all_entries = []

with open("index.ledger", "r") as ind:
    index_lines = ind.readlines()

    for index_line in index_lines:
        file = index_line.split()
        location = file[1]


        with open(location, "r") as fil:
            lines = fil.readlines()
            entries = entry_maker(lines)
        
        for entry in entries:
            all_entries.append(entry)
        
# Convert data from json to dataframe
d_frame = pd.DataFrame(all_entries)
d_frame = d_frame.explode(["account", "credit"])

# Use tabulate to display
my_table = tabulate(d_frame, headers="keys", tablefmt="grid", showindex="False")

print(my_table)
