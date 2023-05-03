def ledger_register(args):
    if args.query == "All":
        print("register All")
    else:
        print(f"register {args.query}")

def ledger_balance(args):
    if args.query == "All":
        print("balance All")
    else:
        print(f"balance {args.query}")
    
def ledger_print(args):
    if args.query == "All":
        print("print All")
    else:
        print(f"print {args.query}")