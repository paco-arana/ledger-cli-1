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
            
            # Separate the string by spaces, isolate the first element
            new_line = line.split(" ", 1)
            date = new_line[0]

            # Everything remaining is the description
            desc = new_line[1]
            desc = desc.replace("\n", "")

            c = 1
            acct = []
            cred = []

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
                        cred.append(new_line[1])
                    # If there is no value there that means we should take the value above
                    except IndexError:
                        credit_previous = flip_symbols(cred[-1])

                        cred.append(credit_previous)
                    
                c += 1

            # Add data to entry
            entry = {
                "date": date,
                "description": desc,
                "account": acct,
                "credit": cred,
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