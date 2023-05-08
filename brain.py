# This file contains the logic for the 'register', 'balance', and 'print' commands.
# Each command is separated into its own function
# This file receives the input from 'main.py' 

from entry_maker import entry_maker
from print_maker import print_maker
import argparse
from tabulate import tabulate
import pandas as pd
# The line below is to avoid warnings being shown in the output
pd.options.mode.chained_assignment = None

def table_maker(args):
    all_entries = []

    with open("index.ledger", "r") as ind:
        index_lines = ind.readlines()

        for index_line in index_lines:
            file = index_line.split()
            location = file[1]

            with open(location, "r") as fil:
                lines = fil.readlines()
                # If a different file was specified using --price-db use that for exchange rates
                if args.price_db:
                    price_file = args.price_db
                    entries = entry_maker(lines, price_file)
                else:
                    entries = entry_maker(lines, "prices_db")
            
            for entry in entries:
                all_entries.append(entry)

    # If the -file command was added we also need to consider that file    
    if args.file:
        what_file = args.file

        with open(what_file, "r") as fil:
                lines = fil.readlines()
                # If a different file was specified using --price-db use that for exchange rates
                if args.price_db:
                    price_file = args.price_db
                    entries = entry_maker(lines, price_file)
                else:
                    entries = entry_maker(lines, "prices_db")

        for entry in entries:
                all_entries.append(entry)

    # Convert data from json to dataframe
    d_frame = pd.DataFrame(all_entries)
    return d_frame.explode(["account", "mov", "u"])

    # Pandas filters examples:
    # d_frame = d_frame.sort_values(by=["date"], ascending=False) # This sorts by date, most recent first

def ledger_register(args):
    df = table_maker(args)

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        
        accounts = accounts.split()
        print(accounts)
        selected_rows = df[df['account'].str.contains('|'.join(accounts))]
        df2 = df[df.index.isin(selected_rows.index)]
    else:
        df2 = df

    df2.loc[:, 'bal'] = df2['mov'].cumsum()
    df2 = df2.assign(u_=df2['u'])

    # Use tabulate to format dataframe into a table
    my_table = tabulate(df2, headers="keys", floatfmt=".2f")

    return(my_table)

def ledger_balance(args):
    df = table_maker(args)

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        
        accounts = accounts.split()
        df2 = df[df['account'].str.contains('|'.join(accounts))]
    else:
        df2 = df

    # Add a balance column, necessary to calculate the total
    df2.loc[:, 'bal'] = df2['mov'].cumsum()
    total = df2['bal'].iloc[-1]

    # create the Total row to append
    total_row = {
        'mov': [total],
        'u': ['$'],
        'account': ['Balance'],
    }
    
    t_df = pd.DataFrame(total_row)

    df2 = df2[["mov", "u", "account"]]

    main_table = tabulate(df2, headers="keys", floatfmt=".2f", showindex=False)
    total_table = tabulate(t_df, floatfmt=".2f", showindex=False)

    return([main_table, total_table])

def ledger_print(args):
    all_entries = []

    with open("index.ledger", "r") as ind:
        index_lines = ind.readlines()

        for index_line in index_lines:
            file = index_line.split()
            location = file[1]


            with open(location, "r") as fil:
                lines = fil.readlines()
                if args.price_db:
                    price_file = args.price_db
                    entries = entry_maker(lines, price_file)
                else:
                    entries = entry_maker(lines, "prices_db")
            
            for entry in entries:
                all_entries.append(entry)
                date = entry["date"]
                description = entry["description"]
                accounts = entry["account"]
                movements = entry["mov"]
                units = entry["u"]

                if args.account:
                    if args.account in accounts[0] or args.account in accounts[1]:
                        print(f"{date} {description}")
                        print(f"    {accounts[0]}   {format_currency(movements[0], units[0])}")
                        print(f"    {accounts[1]}   {format_currency(movements[1], units[1])}")
                else:
                    print(f"{date} {description}")
                    print(f"    {accounts[0]}   {format_currency(movements[0], units[0])}")
                    print(f"    {accounts[1]}   {format_currency(movements[1], units[1])}")
        
def format_currency(amount, unit):
    # Format the amount to two decimal places
    amount_str = f"{amount:.2f}"
    
    # If the amount is negative, insert the dollar sign after the minus symbol
    if amount < 0:
        return f"-{unit}{amount_str[1:]}"
    # Otherwise, insert the dollar sign before the number
    else:
        return f"{unit}{amount_str}"
