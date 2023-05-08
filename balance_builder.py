import pandas as pd

running_balance_value = {}
currencies_used = []

# This function builds the balance column
def balance_builder(d_frame):
    all_values = []
    all_units = []
    for i, row in d_frame.iterrows():
        value = row['mov']
        unit = row['u']
        # If the unit has never been used before it is initialized
        if unit not in currencies_used:
            currencies_used.append(unit)
            running_balance_value[unit] = 0

        # The current balance is the previously stored balance + the value
        balance_val = running_balance_value[unit] + float(value)
        # Stored balance is updated
        running_balance_value[unit] = balance_val

        all_values.append(balance_val)
        all_units.append(unit)

    d_frame["bal"] = all_values
    d_frame["u'"] = all_units

    return(d_frame)

