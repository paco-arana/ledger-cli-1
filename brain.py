from entry_maker import entry_maker
from print_maker import print_maker
import argparse
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
    return d_frame.explode(["account", "mov", "u"])

    # Pandas filters examples:
    # d_frame = d_frame.sort_values(by=["date"], ascending=False) # This sorts by date, most recent first

def ledger_register(args):
    df = table_maker()

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        
        accounts = accounts.split()
        print(accounts)
        df2 = df.query("account like @accounts")
    else:
        df2 = df

    df2['bal'] = df2['mov'].cumsum()

    # Use tabulate to format dataframe into a table
    my_table = tabulate(df2, headers="keys", floatfmt=".2f")

    return(my_table)

def ledger_balance(args):
    df = table_maker()
    df['bal'] = df['mov'].cumsum()

    # return the last item in the 'bal' column as a total 
    total = df['bal'].iloc[-1]

    for_table = {
        "Balance": [total],
    }

    my_table = tabulate(for_table, headers="keys", floatfmt=".2f")

    return(my_table)

def ledger_print():
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
                date = entry["date"]
                description = entry["description"]
                accounts = entry["account"]
                movements = entry["mov"]
                units = entry["u"]

                print(f"{date} {description}")
                print(f"    {accounts[0]}   {movements[0]}{units[0]}")
                print(f"    {accounts[1]}   {movements[1]}{units[1]}")
        