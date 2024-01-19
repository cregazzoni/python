import json

def load_list_books(data_file):

    list_books = []

    # Open JSON file for read
    # list_books variable has a "type: list" (is a list of dictionaries)
    with open(data_file) as fp:
        list_books = json.load(fp)
    fp.close()

    return list_books