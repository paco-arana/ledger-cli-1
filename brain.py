# This file contains the logic for the 'register', 'balance', and 'print' commands.
# Each command is separated into its own function
# This file receives the input from 'main.py' 

from entry_maker import entry_maker
from balance_builder import balance_builder
import argparse
from tabulate import tabulate
import pandas as pd
# The line below is to avoid warnings being shown in the output
pd.options.mode.chained_assignment = None


def table_maker(args):
    all_entries = []

    if args.file:
        file_index = args.file
    else:  
        file_index = "index.ledger"

    with open(f"ledger_files\{file_index}", "r") as ind:
        index_lines = ind.readlines()

        for index_line in index_lines:
            file = index_line.split()
            location = file[1]

            with open(f"ledger_files\{location}", "r") as fil:
                lines = fil.readlines()
                # If a different file was specified using --price-db use that for exchange rates
                entries = entry_maker(lines)
            
            for entry in entries:
                all_entries.append(entry)

    # Convert data from json to dataframe
    d_frame = pd.DataFrame(all_entries)
    return(d_frame.explode(["account", "mov", "u"]))


def ledger_register(args):
    df = table_maker(args)

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        
        accounts = accounts.split()
        print(accounts)
        selected_rows = df[df['account'].str.contains('|'.join(accounts))]
        df1 = df[df.index.isin(selected_rows.index)]
    else:
        df1 = df

    # if the --sort flag was used the result has to be sorted
    if args.sort == "date" or args.sort == "d":
        df1 = df1.sort_values(by=["date"], ascending=False)

    # The balance column is built:
    df2 = balance_builder(df1) 

    # Don't display duplicated info:
    is_duplicated = df2.duplicated(subset=["date", "description"])
    df2.loc[is_duplicated, ["date", "description"]] = ""

    # Use tabulate to format dataframe into a table
    my_table = tabulate(df2, headers="keys", floatfmt=".2f", showindex=False)

    return(my_table)


def ledger_balance(args):
    df = table_maker(args)

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        accounts = accounts.split()
        df1 = df[df['account'].str.contains('|'.join(accounts))]
    else:
        df1 = df

    # if the --sort flag was used the result has to be sorted
    if args.sort == "date" or args.sort == "d":
        df1 = df1.sort_values(by=["date"], ascending=False)

    # The balance column is built:
    df1 = balance_builder(df1) 

    # Get the final balance rows
    df2 = df1.drop_duplicates(subset="u'", keep='last')

    # Get rid of the columns we don't want to output
    df1 = df1[["mov", "u", "account"]]
    df2 = df2[["bal", "u'"]]

    main_table = tabulate(df1, headers="keys", floatfmt=".2f", showindex=False)
    total_table = tabulate(df2, floatfmt=".2f", showindex=False)

    return([main_table, total_table])


def ledger_print(args):
    all_entries = []

    if args.file:
        file_index = args.file
    else:  
        file_index = "index.ledger"

    with open(f"ledger_files\{file_index}", "r") as ind:
        index_lines = ind.readlines()

        for index_line in index_lines:
            file = index_line.split()
            location = file[1]


            with open(f"ledger_files\{location}", "r") as fil:
                lines = fil.readlines()
                entries = entry_maker(lines)
            
            for entry in entries:
                all_entries.append(entry)
                date = entry["date"]
                description = entry["description"]
                accounts = entry["account"]
                movements = (entry["mov"])
                units = entry["u"]
                if args.account:
                    if args.account in accounts[0] or args.account in accounts[1]:
                        print(f"{date} {description}")
                        print(f"    {accounts[0]}   {format_currency(float(movements[0]), units[0])}")
                        print(f"    {accounts[1]}   {format_currency(float(movements[1]), units[1])}")
                else:
                    print(f"{date} {description}")
                    print(f"    {accounts[0]}   {format_currency(float(movements[0]), units[0])}")
                    print(f"    {accounts[1]}   {format_currency(float(movements[1]), units[1])}")
        

def format_currency(amount, unit):
    # Format the amount to two decimal places
    amount_str = f"{amount:.2f}"
    
    if unit != "$":
        # Inser the currency symbol after the amount
        return f"{amount_str} {unit}"

    else:
        # If the amount is negative, insert the dollar sign after the minus symbol
        if amount < 0:
            return f"-{unit}{amount_str[1:]}"
        # Otherwise, insert the dollar sign before the number
        else:
            return f"{unit}{amount_str}"
