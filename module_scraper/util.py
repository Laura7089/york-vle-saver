def to_key(string):
    return "".join(c for c in string.lower()
                   if c.isalnum() or c == ' ').replace(" ", "_")
