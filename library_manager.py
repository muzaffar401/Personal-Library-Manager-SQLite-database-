import sqlite3
import uuid
import argparse

# Define the database file name
DATABASE_FILE = "library.db"

# Function to initialize the database
def init_database():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Create the 'books' table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,          -- Unique identifier for the book
                title TEXT NOT NULL,          -- Title of the book
                author TEXT NOT NULL,        -- Author of the book
                year INTEGER NOT NULL,        -- Publication year of the book
                genre TEXT NOT NULL,          -- Genre of the book
                content TEXT NOT NULL,       -- Content or description of the book
                read INTEGER NOT NULL         -- Read status (0 for unread, 1 for read)
            )
        ''')
        # Commit the transaction
        conn.commit()
    except sqlite3.Error as e:
        # Print any errors that occur during database initialization
        print(f"Error initializing database: {e}")
    finally:
        # Close the database connection
        conn.close()

# Function to get a database connection
def get_db_connection():
    return sqlite3.connect(DATABASE_FILE, isolation_level=None)

# Function to get non-empty input from the user
def get_non_empty_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Error: This field cannot be blank. Please try again.")

# Function to get a valid year input from the user
def get_valid_year(prompt):
    while True:
        year = input(prompt).strip()
        if year.isdigit():
            return int(year)
        print("Error: Publication year must be a valid number. Please try again.")

# Function to add a new book to the database
def add_book():
    # Get book details from the user
    title = get_non_empty_input("Enter the title of the book: ")
    author = get_non_empty_input("Enter the author of the book: ")
    year = get_valid_year("Enter the publication year of the book: ")
    genre = get_non_empty_input("Enter the genre of the book: ")
    content = get_non_empty_input("Enter the content of the book: ")
    read_status = input("Have you read this book? (yes/no): ").lower() == "yes"
    book_id = str(uuid.uuid4().hex)[:6]  # Generate a unique ID for the book

    try:
        # Connect to the database
        conn = get_db_connection()
        # Insert the new book into the 'books' table
        conn.execute('''
            INSERT INTO books (id, title, author, year, genre, content, read)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, title, author, year, genre, content, int(read_status)))
        conn.commit()
        print(f"Book added successfully! ID: {book_id}")
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")
    finally:
        conn.close()

# Function to update an existing book in the database
def update_book():
    # Get the ID of the book to update
    book_id = get_non_empty_input("Enter the ID of the book to update: ")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fetch the book details from the database
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book not found!")
            return

        # Get updated details from the user, allowing empty input to keep existing values
        title = get_non_empty_input(f"Enter new title ({book[1]}): ", allow_empty=True) or book[1]
        author = get_non_empty_input(f"Enter new author ({book[2]}): ", allow_empty=True) or book[2]
        year_input = input(f"Enter new year ({book[3]}): ").strip()
        year = int(year_input) if year_input.isdigit() else book[3]
        genre = get_non_empty_input(f"Enter new genre ({book[4]}): ", allow_empty=True) or book[4]
        content = get_non_empty_input(f"Enter new content ({book[5]}): ", allow_empty=True) or book[5]
        read_status = input(f"Have you read this book? (yes/no, current: {'yes' if book[6] else 'no'}): ").lower()
        read_status = 1 if read_status == "yes" else 0

        # Update the book details in the database
        cursor.execute('''
            UPDATE books
            SET title = ?, author = ?, year = ?, genre = ?, content = ?, read = ?
            WHERE id = ?
        ''', (title, author, year, genre, content, read_status, book_id))
        conn.commit()
        print("Book updated successfully!")
    except sqlite3.Error as e:
        print(f"Error updating book: {e}")
    finally:
        conn.close()

# Function to remove a book from the database
def remove_book():
    # Get the ID of the book to remove
    book_id = get_non_empty_input("Enter the ID of the book to remove: ")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Delete the book from the database
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Book removed successfully!")
        else:
            print("Book not found!")
    except sqlite3.Error as e:
        print(f"Error removing book: {e}")
    finally:
        conn.close()

# Function to search for a book by title, author, or ID
def search_book():
    search_term = get_non_empty_input("Enter the title, author, or ID to search: ", allow_empty=False)

    try:
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM books 
            WHERE id = ? OR title LIKE ? OR author LIKE ?
        ''', (search_term, f'%{search_term}%', f'%{search_term}%'))
        results = cursor.fetchall()
        if results:
            for book in results:
                print(f"""
                Title: {book[1]}
                Author: {book[2]}
                Year: {book[3]}
                Genre: {book[4]}
                Read: {'✅ Read' if book[6] else '❌ Unread'}
                ID: {book[0]}
                Content: {book[5]}
                """)
        else:
            print("No matching books found!")
    except sqlite3.Error as e:
        print(f"Error searching book: {e}")
    finally:
        conn.close()

# Function to display statistics about the books in the library
def display_statistics():
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT COUNT(*) FROM books')
        total_books = cursor.fetchone()[0]
        cursor = conn.execute('SELECT COUNT(*) FROM books WHERE read = 1')
        read_books = cursor.fetchone()[0]
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        print(f"Total books: {total_books}")
        print(f"Percentage read: {read_percentage:.1f}%")
    except sqlite3.Error as e:
        print(f"Error displaying statistics: {e}")
    finally:
        conn.close()

# Function to display all books in the library
def display_all_books():
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM books')
        books = cursor.fetchall()
        if books:
            for book in books:
                print(f"""
                Title: {book[1]}
                Author: {book[2]}
                Year: {book[3]}
                Genre: {book[4]}
                Read: {'✅ Read' if book[6] else '❌ Unread'}
                ID: {book[0]}
                Content: {book[5]}
                """)
        else:
            print("No books found in the library!")
    except sqlite3.Error as e:
        print(f"Error displaying books: {e}")
    finally:
        conn.close()

# Main function to handle command-line arguments and execute the appropriate function
def main():
    init_database()
    parser = argparse.ArgumentParser(description="Personal Library Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("add").set_defaults(func=add_book)
    subparsers.add_parser("remove").set_defaults(func=remove_book)
    subparsers.add_parser("search").set_defaults(func=search_book)
    subparsers.add_parser("display").set_defaults(func=display_all_books)
    subparsers.add_parser("stats").set_defaults(func=display_statistics)
    subparsers.add_parser("update").set_defaults(func=update_book)

    args = parser.parse_args()
    if args.command:
        args.func()

if __name__ == "__main__":
    main()