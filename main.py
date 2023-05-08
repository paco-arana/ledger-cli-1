import argparse
from brain import ledger_balance, ledger_print, ledger_register
from register_alt import ledger_register_alt

parser = argparse.ArgumentParser(
    prog='Ledger CLI',
    description='Ledger is a simple bookkeeping tool based on double entry accounting',
    epilog='Made by Jose Arana for the Encora apprenticeship program'
)

parser.add_argument("command", type=str, choices=["register", "reg", "r", "balance", "bal", "b", "print", "pr"],
                    help="Use 'register' to show every transaction and a running balance. Use 'balance' to show balance only. Use 'print' to show input files formatted uniformly.")

parser.add_argument("-a", "--account", type=str, metavar="STRING",
                    help="Narrow search to selected accounts")

parser.add_argument("-s", "--sort", type=str, choices=["date", "d"],
                    help="Used to sort the results, only sorting options currently available are date-related")

parser.add_argument("-p", "--price-db", type=str, metavar="FILE",
                    help="Requires a file to be specified, when used the results will be shown in USD according to the exchange rate")

parser.add_argument("-f", "--file", type=str, metavar="FILE",
                    help="Specify what file to use as an index")

args = parser.parse_args()

# Depending on what command was called, execute a different function from 'brain.py'
if args.command == "register" or args.command == "reg" or args.command == "r":
    if args.price_db:
        # The code when using price-db is so different from normal that it was easier to have it in a different file.
        print(ledger_register_alt(args))
    else:
        print(ledger_register(args))
elif args.command == "balance" or args.command == "bal" or args.command == "b":
    balance = ledger_balance(args)
    # If accounts were specified they should be shown along the total
    if args.account:
        print(balance[0])
        print(balance[1])
    # Otherwise show the total alone
    else:
        print(balance[1])
elif args.command == "print" or args.command == "pr":
    ledger_print(args)
