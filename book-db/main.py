import json

def menu():

    message = ("1) View the books collection\n"
               "2) Filter books by author\n"
               "3) Enter new book\n"
               "4) Exit the program\n"
               "> Enter your action: ")
    choice = input(message)

    if choice == "1":
        view(data_file)
    elif choice == "2":
        select(data_file)
    elif choice == "3":
        insert(data_file)
    elif choice == "4":
        exit(0)
    else:
        menu()


def view(data_file):

    list_books = []

    # Open JSON file for read
    # list_books variable has a "type: list" (is a list of dictionaries)
    with open(data_file) as fp:
        list_books = json.load(fp)
    fp.close()

    for book in list_books:
        title = book["Title"]
        author = book["Author"]
        rate = book["Rate"]
        print("Title: " + title)
        print("Author: " + author)
        print("Rate: " + str(rate))
        print("")

    menu()


def insert(data_file):

    list_books = []

    # Open JSON file for read, and then close it
    # Variable list_books is a "type: list" (a list of dictionaries)
    with open(data_file) as fp:
        list_books = json.load(fp)
    fp.close()

    # Info to insert new book
    title = input("Enter the title: ")
    author = input("Enter the author: ")
    rate = 0
    while rate < 1 or rate > 5:
        rate = int(input("Enter your rating (from 1 to 5): "))

    # Check if title already exists
    for book in list_books:
        if title == book["Title"]:
            id = book["ID"]
            print("<!> Title already exists: ")
            print_book(id)
            menu()

    # Check available id
    list_id = []
    for book in list_books:
        list_id.append(book["ID"])
    new_id = int((max(list_id))) + 1

    # Append new dictionary to book list
    list_books.append({
        "ID": new_id,
        "Title": title,
        "Author": author,
        "Rate": rate
    })

    # Write a new file with the updated list of books
    with open(data_file, 'w') as json_file:
        json.dump(list_books, json_file, indent=4, separators=(',', ': '))
    json_file.close()

    # Back to menu
    print("")
    menu()


def select(data_file):

    list_books = []

    # Open JSON file for read, and then close it
    # Variable list_books is a "type: list" (a list of dictionaries)
    with open(data_file) as fp:
        list_books = json.load(fp)
    fp.close()

    author = input("Enter the author: ")
    count = 0
    print("")

    # Check author in book list
    for book in list_books:
        if author == book["Author"]:
            id = book["ID"]
            print_book(id)
            count += 1

    if count == 0:
        print("No books found for author: " + author)
    elif count == 1:
        print("-> Found " + str(count) + " book with author " + author)
    else:
        print("-> Found " + str(count) + " books with author " + author)

    # Back to menu
    print("")
    menu()


def print_book(id):

    list_books = []

    # Open JSON file for read, and then close it
    # Variable list_books is a "type: list" (a list of dictionaries)
    with open(data_file) as fp:
        list_books = json.load(fp)
    fp.close()

    # Find ID in list books
    for book in list_books:
        if id == book["ID"]:
            title = book["Title"]
            author = book["Author"]
            rate = book["Rate"]
            print("Title: " + title)
            print("Author: " + author)
            print("Rate: " + str(rate))
            print("")


data_file = "data.json"
menu()
