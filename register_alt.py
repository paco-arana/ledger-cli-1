from entry_maker import flip_symbols
from tabulate import tabulate
import pandas as pd

def ledger_register_alt(args):
    print(table_maker(args))

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
                entries = entry_maker(lines, "prices_db")

            for entry in entries:
                all_entries.append(entry)

    # Convert data from json to dataframe
    d_frame = pd.DataFrame(all_entries)
    d_frame = d_frame.explode(["account", "mov", "u"])

    # if an account or list of accounts is given they have to be used to filter the table
    if args.account:
        accounts = args.account
        
        accounts = accounts.split()
        selected_rows = d_frame[d_frame['account'].str.contains('|'.join(accounts))]
        d_frame = d_frame[d_frame.index.isin(selected_rows.index)]

    # if the --sort flag was used the result has to be sorted
    if args.sort == "date" or args.sort == "d":
        d_frame = d_frame.sort_values(by=["date"], ascending=False)

    # calculate the running balance column using "cumulative sum" cumsum()
    d_frame['bal'] = d_frame['mov'].cumsum()
    d_frame["u'"] = d_frame ["u"]

    # Don't display duplicated info:
    is_duplicated = d_frame.duplicated(subset=["date", "description"])
    d_frame.loc[is_duplicated, ["date", "description"]] = ""

    # Use tabulate to display both dataframes together
    my_table = tabulate(d_frame, headers="keys", floatfmt=".2f", showindex=False)

    return(my_table)

def entry_maker(lines, prices="prices_db"):
    # Imports the exchange rates specified for use later
    with open(f"ledger_files\{prices}", "r") as f:
        ex_rates = f.readlines()

    # create an empty list to store every entry 
    entries = []
    entry = {}
    # iterate through each line and extract the necessary information
    for i, line in enumerate(lines):
        # Always ignore the first line
        if line.startswith(";"):
            continue
        # Create a new entry if a line starts with a date
        if line.startswith("20") or line.startswith("19"):
            # If entry is not empty, append it:
            if entry:
                entries.append(entry)
            
            # Separate the string by spaces, isolate the date
            new_line = line.split(" ", 1)
            date = new_line[0]
            # Process the date string so that it fits the format YYYY/MM/DD
            split_date = date.split("/")
            year = split_date[0]
            month = split_date[1]
            day = split_date[2]
            if len(month) < 2:
                month = "0" + month 
            if len(day) < 2:
                day = "0" + day 
            date = year + "/" + month + "/" + day
            # Everything remaining is the description
            desc = new_line[1]
            desc = desc.replace("\n", "")
            # Reset counter and all lists
            c = 1
            acct = []
            movt = []
            movt_value = []
            movt_units = []

            while i+c < len(lines):
                if lines[i+c].startswith("20") or lines[i+c].startswith("19"):
                    break
                else:
                    text_line = lines[i+c]
                    
                    # Separate account from credit using the tabs (\t)
                    new_line = text_line.split("\t")
                    # Remove any empty strings from the line 
                    new_line = list(filter(None, new_line))
                    # Remove any breaks (\n) from the strings
                    for j in range(len(new_line)):
                        new_line[j] = new_line[j].rstrip()
                    # The element at index 0 is the account:    
                    acct.append(new_line[0])
                    # The element at index 1 is the credit:
                    try:
                        movt.append(new_line[1])
                    # If there is no value there that means we should take the value above
                    except IndexError:
                        movement_previous = flip_symbols(movt[-1])
                        movt.append(movement_previous)
                c += 1
            # Separate movement values and units
            for val in movt:
                val_list = val.split()
                if len(val_list) > 1: # For units other than "$"
                    val = val_list[0]
                    curr = val_list[1]
                    for ex in ex_rates[2:]:
                        if curr in ex:
                            rate_split = ex.split("$")
                            rate = float(rate_split[1])

                    prev_val = float(val_list[0])
                    new_val = prev_val * rate

                    movt_value.append(new_val)
                    movt_units.append("$")
                else:
                    val = val_list[0]
                    val = val.replace("$", "")
                    movt_value.append(float(val))
                    movt_units.append("$")

            # Build balance column (Obsolete)
            """
            bal_columns = build_bal(movt_value, movt_units, prices)
            bal_value = bal_columns[0]
            bal_units = bal_columns[1]
            """

            # Add data to entry
            entry = {
                "date": date,
                "description": desc,
                "account": acct,
                "mov": movt_value,
                "u": movt_units,
                # "bal": bal_value,
                # "u'": bal_units,
            }

    # Append the final entry
    if entry:
        entries.append(entry)
    # print the list of entries
    return(entries)