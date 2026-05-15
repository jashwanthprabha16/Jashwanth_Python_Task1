# Library Book Management System

def add_book(catalog, book_id, title, author, year):
    catalog[book_id] = (title, author, year)
    print(f'Book added: [{book_id}] {title} by {author} ({year})')

def borrow_book(catalog, borrowed_books, book_id):
    if book_id not in catalog:
        print(f'Book ID {book_id} does not exist in catalog.')
    elif book_id in borrowed_books:
        print(f'Book ID {book_id} is already borrowed.')
    else:
        borrowed_books.append(book_id)
        print(f'Book ID {book_id} borrowed successfully.')

def return_book(borrowed_books, book_id):
    if book_id in borrowed_books:
        borrowed_books.remove(book_id)
        print(f'Book ID {book_id} returned successfully.')
    else:
        print(f'Book ID {book_id} was not borrowed.')

def register_member(members, member_id):
    members.add(member_id)  # set silently ignores duplicates

def show_available(catalog, borrowed_books):
    print('\nAvailable Books:')
    for book_id, details in catalog.items():
        if book_id not in borrowed_books:
            title, author, year = details
            print(f'  [{book_id}] {title} by {author} ({year})')

def main():
    catalog = {}
    borrowed_books = []
    members = set()

    # Add 4 books
    print('--- Adding Books ---')
    add_book(catalog, 101, 'Python Crash Course', 'Eric Matthes', 2019)
    add_book(catalog, 102, 'Clean Code', 'Robert C. Martin', 2008)
    add_book(catalog, 103, 'The Pragmatic Programmer', 'Andrew Hunt', 1999)
    add_book(catalog, 104, 'Automate the Boring Stuff', 'Al Sweigart', 2020)

    # Register 3 members (one duplicate)
    print('\n--- Registering Members ---')
    register_member(members, 'M001')
    register_member(members, 'M002')
    register_member(members, 'M003')
    register_member(members, 'M001')  # duplicate - silently ignored
    print(f'Members registered: {members}')

    # Borrow 2 books
    print('\n--- Borrowing Books ---')
    borrow_book(catalog, borrowed_books, 101)
    borrow_book(catalog, borrowed_books, 103)
    borrow_book(catalog, borrowed_books, 101)  # already borrowed - blocked

    # Return 1 book
    print('\n--- Returning Books ---')
    return_book(borrowed_books, 101)

    # Show available books
    show_available(catalog, borrowed_books)

main()