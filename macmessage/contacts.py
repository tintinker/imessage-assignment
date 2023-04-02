def contacts(text_file, sender):
    name_number = {}
    number_name = {}

    with open(text_file, "r") as f:
        for line in f:
            if "+" in line and not "#" in line:
                name_number[line.split()[0]] = line.split()[1]

    number_name = dict((val, key) for key, val in name_number.items())
    number_name['sender'] = sender

    return (name_number, number_name)
