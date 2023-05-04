import argparse
from brain import table_maker
from tabulate import tabulate

parser = argparse.ArgumentParser(description="Ledger")

parser.add_argument("register", type=str)

args = parser.parse_args()

if args.register == True:
    display = table_maker()
    tabular_data = display[0]
    balance_total = display[1]
    balance_total = "%.2f" % balance_total


            

    if len(display) > 1:
        print(display[0])
        print("------------------------")
        print(f"Balance: {balance_total}")

    else:
        print(display[0])
