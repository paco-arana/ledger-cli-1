# This file takes the lines of each ledger file and builds a dictionary with the data
# This dictionary is passed to the 'brain.py' file where it is converted to a pandas dataframe

running_balance_value = [0]
currencies_used = ["$"]

def entry_maker(lines):
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
                    
                    # Separate account from money using the tabs (\t)
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
                    movt_value.append(val)
                    movt_units.append(curr)
                else:
                    val = val_list[0]
                    val = val.replace("$", "")
                    movt_value.append(float(val))
                    movt_units.append("$")

            # Previously used to build the balance column (Obsolete)
            # bal_columns = build_bal(movt_value, movt_units)
            # bal_value = bal_columns[0]
            # bal_units = bal_columns[1]

            # Add data to entry
            entry = {
                "date": date,
                "description": desc,
                "account": acct,
                "mov": movt_value,
                "u": movt_units,
                # "bal": bal_value,
                # "u'": bal_units
            }

    # Append the final entry
    if entry:
        entries.append(entry)

    # print the list of entries
    return(entries)


# This is just to change from positive to negative values
def flip_symbols(string):
    if string.startswith("-"):
        return string[1:]
    else:
        return "-" + string
    
