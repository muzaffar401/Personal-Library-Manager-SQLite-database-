import sqlite3  # Import SQLite module for database operations
import uuid  # Import the uuid module to generate unique IDs for books
import argparse  # Import the argparse module to handle command-line arguments

# Database configuration
DATABASE_FILE = "library.db"  # Define the name of the SQLite database file

def init_database():
    """
    Initialize the database and create the 'books' table if it doesn't exist.
    This function ensures that the database is set up correctly before any operations are performed.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)  # Connect to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,  # Unique ID for each book
                title TEXT NOT NULL,  # Title of the book
                author TEXT NOT NULL,  # Author of the book
                year INTEGER NOT NULL,  # Publication year of the book
                genre TEXT NOT NULL,  # Genre of the book
                content TEXT NOT NULL,  # Content or description of the book
                read BOOLEAN NOT NULL  # Whether the book has been read (True/False)
            )
        ''')  # Execute SQL command to create the 'books' table if it doesn't exist
        conn.commit()  # Commit the transaction to save changes
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")  # Handle any errors that occur during database initialization
    finally:
        if conn:
            conn.close()  # Close the database connection to free resources

def get_db_connection():
    """
    Create and return a database connection.
    This function is used to establish a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_FILE, isolation_level=None)  # Return a connection object with autocommit mode

def get_non_empty_input(prompt):
    """
    Prompt the user for input and ensure that the input is not empty.
    This function is used to validate user input for fields that cannot be blank.
    """
    while True:
        value = input(prompt).strip()  # Get user input and remove leading/trailing whitespace
        if value:
            return value  # Return the input if it's not empty
        print("Error: This field cannot be blank. Please try again.")  # Prompt the user again if the input is empty

def get_valid_year(prompt):
    """
    Prompt the user for a valid publication year.
    This function ensures that the input is a valid integer representing a year.
    """
    while True:
        year = input(prompt).strip()  # Get user input and remove leading/trailing whitespace
        if year.isdigit():  # Check if the input is a valid number
            return int(year)  # Return the input as an integer if it's valid
        print("Error: Publication year must be a valid number. Please try again.")  # Prompt the user again if the input is invalid

def add_book():
    """
    Add a new book to the library.
    This function collects book details from the user and inserts them into the database.
    """
    title = get_non_empty_input("Enter the title of the book: ")  # Get the book title
    author = get_non_empty_input("Enter the author of the book: ")  # Get the book author
    year = get_valid_year("Enter the publication year of the book: ")  # Get the publication year
    genre = get_non_empty_input("Enter the genre of the book: ")  # Get the book genre
    content = get_non_empty_input("Enter the content of the book: ")  # Get the book content
    read_status = input("Have you read this book? (yes/no): ").lower() == "yes"  # Get the read status (True/False)
    book_id = str(uuid.uuid4().int)[:3]  # Generate a unique 3-digit ID for the book using UUID
    
    try:
        conn = get_db_connection()  # Establish a database connection
        conn.execute('''
            INSERT INTO books (id, title, author, year, genre, content, read)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, title, author, year, genre, content, read_status))  # Insert the book details into the database
        conn.commit()  # Commit the transaction to save changes
        print(f"Book added successfully! ID: {book_id}")  # Notify the user that the book was added
    except sqlite3.Error as e:
        print(f"Error adding book: {e}")  # Handle any errors that occur during the insertion
    finally:
        if conn:
            conn.close()  # Close the database connection

def remove_book():
    """
    Remove a book from the library by its ID.
    This function deletes a book from the database based on the provided ID.
    """
    book_id = input("Enter the ID of the book to remove: ")  # Get the book ID from the user
    try:
        conn = get_db_connection()  # Establish a database connection
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))  # Delete the book with the specified ID
        conn.commit()  # Commit the transaction to save changes
        if cursor.rowcount > 0:  # Check if any rows were affected (i.e., if the book was found and deleted)
            print("Book removed successfully!")  # Notify the user that the book was removed
        else:
            print("Book not found!")  # Notify the user if the book was not found
    except sqlite3.Error as e:
        print(f"Error removing book: {e}")  # Handle any errors that occur during the deletion
    finally:
        if conn:
            conn.close()  # Close the database connection

def search_book():
    """
    Search for a book by title, author, or ID.
    This function allows the user to search for a book using a search term and displays the results.
    """
    search_term = input("Enter the title, author, or ID to search: ").strip()  # Get the search term from the user
    if not search_term:
        print("Book not found!")  # Notify the user if the search term is empty
        return
    
    try:
        conn = get_db_connection()  # Establish a database connection
        cursor = conn.execute('''
            SELECT * FROM books 
            WHERE id = ? OR title LIKE ? OR author LIKE ?
        ''', (search_term, f'%{search_term}%', f'%{search_term}%'))  # Search for books matching the search term
        results = cursor.fetchall()  # Fetch all matching records
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
                """)  # Display the details of each matching book
        else:
            print("No matching books found!")  # Notify the user if no books were found
    except sqlite3.Error as e:
        print(f"Error searching book: {e}")  # Handle any errors that occur during the search
    finally:
        if conn:
            conn.close()  # Close the database connection

def display_statistics():
    """
    Display library statistics, including the total number of books and the percentage of books read.
    This function provides an overview of the library's contents.
    """
    try:
        conn = get_db_connection()  # Establish a database connection
        cursor = conn.execute('SELECT COUNT(*) FROM books')  # Get the total number of books
        total_books = cursor.fetchone()[0]  # Fetch the result
        cursor = conn.execute('SELECT COUNT(*) FROM books WHERE read = 1')  # Get the number of books that have been read
        read_books = cursor.fetchone()[0]  # Fetch the result
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0  # Calculate the percentage of books read
        print(f"Total books: {total_books}")  # Display the total number of books
        print(f"Percentage read: {read_percentage:.1f}%")  # Display the percentage of books read
    except sqlite3.Error as e:
        print(f"Error displaying statistics: {e}")  # Handle any errors that occur during the statistics calculation
    finally:
        if conn:
            conn.close()  # Close the database connection

def display_all_books():
    """
    Display all books in the library.
    This function lists all the books stored in the database.
    """
    try:
        conn = get_db_connection()  # Establish a database connection
        cursor = conn.execute('SELECT * FROM books')  # Get all books from the database
        books = cursor.fetchall()  # Fetch all records
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
                """)  # Display the details of each book
        else:
            print("No books found in the library!")  # Notify the user if no books are found
    except sqlite3.Error as e:
        print(f"Error displaying books: {e}")  # Handle any errors that occur during the display
    finally:
        if conn:
            conn.close()  # Close the database connection

def main():
    """
    Main function to handle command-line arguments and execute the appropriate function.
    This function sets up the command-line interface and processes user commands.
    """
    init_database()  # Initialize the database
    parser = argparse.ArgumentParser(description="Personal Library Manager")  # Create an argument parser
    subparsers = parser.add_subparsers(dest="command")  # Add subparsers for different commands
    subparsers.add_parser("add", help="Add a new book")  # Add a subparser for the 'add' command
    subparsers.add_parser("remove", help="Remove a book")  # Add a subparser for the 'remove' command
    subparsers.add_parser("search", help="Search for a book")  # Add a subparser for the 'search' command
    subparsers.add_parser("display", help="Display all books")  # Add a subparser for the 'display' command
    subparsers.add_parser("stats", help="Display library statistics")  # Add a subparser for the 'stats' command
    args = parser.parse_args()  # Parse the command-line arguments
    if args.command == "add":
        add_book()  # Call the 'add_book' function if the 'add' command is used
    elif args.command == "remove":
        remove_book()  # Call the 'remove_book' function if the 'remove' command is used
    elif args.command == "search":
        search_book()  # Call the 'search_book' function if the 'search' command is used
    elif args.command == "display":
        display_all_books()  # Call the 'display_all_books' function if the 'display' command is used
    elif args.command == "stats":
        display_statistics()  # Call the 'display_statistics' function if the 'stats' command is used
    else:
        parser.print_help()  # Display help information if no valid command is provided

if __name__ == "__main__":
    main()  # Execute the main function when the script is run