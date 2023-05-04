import argparse
from brainTest import ledger_balance, ledger_print, ledger_register

parser = argparse.ArgumentParser(
    prog='Ledger CLI',
    description='Ledger is a simple bookkeeping tool based on double entry accounting',
    epilog='Made by Jose Arana for the Encora apprenticeship program'
)

parser.add_argument("command", type=str, choices=["register", "balance", "print"],
                    help="Use 'register' to show every transaction and a running balance. Use 'balance' to show balance only. Use 'print' for printing I guess")

parser.add_argument("-q", "--query", type=str, metavar="STRING",
                    help="Used to add a query and narrow down the entries shown.")

parser.add_argument("-s", "--sort", type=str, )


args = parser.parse_args()

if args.query:
    print("Yes")
else:
    print("No")
"""
if args.command == "register":
    ledger_register(args)
elif args.command == "balance":
    ledger_balance(args)
elif args.command == "print":
    ledger_print(args)
"""
