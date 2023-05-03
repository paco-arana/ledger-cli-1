import argparse
from brain import ledger_balance, ledger_print, ledger_register

parser = argparse.ArgumentParser(
                    prog='Ledger CLI',
                    description='Ledger is a simple bookkeeping tool based on double entry accounting',
                    epilog='Made by Jose Arana for the Encora apprenticeship program')

# parser.add_argument("command", type=str, choices=["register", "balance", "print"])

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--register", type=str, required=False)
group.add_argument("--balance", type=str, required=False)
group.add_argument("--print", type=str, required=False)




args = parser.parse_args()

if args.command == "register":
    ledger_register(args)
elif args.command == "balance":
    ledger_balance(args)
elif args.command == "print":
    ledger_print(args)

