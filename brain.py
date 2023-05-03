from entry_maker import entry_maker
from tabulate import tabulate
import pandas as pd

def table_maker():
    all_entries = []

    with open("index.ledger", "r") as ind:
        index_lines = ind.readlines()

        for index_line in index_lines:
            file = index_line.split()
            location = file[1]


            with open(location, "r") as fil:
                lines = fil.readlines()
                entries = entry_maker(lines, "prices_db")
            
            for entry in entries:
                all_entries.append(entry)
            
    # Convert data from json to dataframe
    d_frame = pd.DataFrame(all_entries)
    d_frame = d_frame.explode(["account", "mov", "u"])

    # Pandas filters examples:
    # d_frame = d_frame.sort_values(by=["date"], ascending=False) # This sorts by date, most recent first

    # calculate the running balance column using "cumulative sum" cumsum()
    d_frame['bal'] = d_frame['mov'].cumsum()

    # add a total row for the running balance column
    total = d_frame['bal'].iloc[-1]
    
    # Use tabulate to display both dataframes together
    my_table = tabulate(d_frame, headers="keys", floatfmt=".2f")

    return([my_table, total])
