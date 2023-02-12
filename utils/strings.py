def is_positive_number(s):
    try:
        number_string = float(s)
    except ValueError:
        return False
    return number_string > 0
