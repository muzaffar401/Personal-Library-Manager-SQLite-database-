# Personal Library Manager

Welcome to the **Personal Library Manager**! This is a simple command-line application that helps you manage your personal library of books. You can add, remove, search, and display books, as well as view statistics about your library. The application uses an SQLite database to store all the book information.

---

## Features

- **Add a Book**: Add a new book to your library by providing details like title, author, publication year, genre, content, and read status.
- **Remove a Book**: Remove a book from your library using its unique ID.
- **Search for a Book**: Search for a book by its title, author, or ID.
- **Display All Books**: View a list of all the books in your library.
- **Library Statistics**: View statistics like the total number of books and the percentage of books you've read.
- **View Database Table**: Display the structure of the `books` table in SQLite.
- **Export Data to CSV**: Download all book records as a CSV file.

---

## How to Use the Project

### Prerequisites
- **Python 3.x**: Make sure you have Python installed on your system.
- **SQLite**: The project uses SQLite, which is included with Python by default.

### Installation
1. **Download the Project**:
   - Download the project files and extract them to a folder on your computer.

2. **Run the Script**:
   - Open a terminal or command prompt and navigate to the project folder.
   - Run the Python script:
     ```bash
     python library_manager.py
     ```

---

## Commands

The project uses command-line arguments to perform different actions. Here are the available commands:

### 1. **Add a Book**
   - Command: `python library_manager.py add`
   - Description: Add a new book to your library.
   - Example:
     ```bash
     python library_manager.py add
     ```

### 2. **Remove a Book**
   - Command: `python library_manager.py remove`
   - Example:
     ```bash
     python library_manager.py remove
     ```

### 3. **Search for a Book**
   - Command: `python library_manager.py search`
   - Example:
     ```bash
     python library_manager.py search
     ```

### 4. **Display All Books**
   - Command: `python library_manager.py display`
   - Example:
     ```bash
     python library_manager.py display
     ```

### 5. **View Library Statistics**
   - Command: `python library_manager.py stats`
   - Example:
     ```bash
     python library_manager.py stats
     ```

### 6. **View Database Table Structure**
   - Open SQLite shell:
     ```bash
     sqlite3 library.db
     ```
   - View the table format:
     ```sql
     PRAGMA table_info(books);
     ```

### 7. **Show All Book Records in Database**
   - Run this command in SQLite shell:
     ```sql
     SELECT * FROM books;
     ```

### 8. **Export Database to CSV**
   - Run SQLite and execute the following commands:
     ```sql
     .headers on
     .mode csv
     .output books.csv
     SELECT * FROM books;
     .output stdout
     ```
   - This will create a `books.csv` file in the current directory.

---

## About the Database

The project uses an **SQLite database** to store all the book information. SQLite is a lightweight, file-based database that doesn't require any additional setup. Here's how the database works in this project:

### Database File
- The database is stored in a file named `library.db`.
- This file is automatically created when you run the script for the first time.

### Database Table
- The database contains a single table named `books`.
- The table has the following columns:
  1. **`id`**: A unique 3-digit ID for each book (automatically generated).
  2. **`title`**: The title of the book.
  3. **`author`**: The author of the book.
  4. **`year`**: The publication year of the book.
  5. **`genre`**: The genre of the book.
  6. **`content`**: A description or summary of the book.
  7. **`read`**: A boolean value (`True` or `False`) indicating whether the book has been read.

### How the Database is Created
- When you run the script for the first time, the `init_database()` function is called.
- This function creates the `books` table if it doesn't already exist.

---

## Troubleshooting

- **Database Errors**: If you encounter errors related to the database, make sure the `library.db` file is not corrupted. You can delete the file and run the script again to create a new database.
- **Command Not Working**: Ensure you're using the correct command and that Python is installed correctly.

---

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Your contributions are welcome!

---

## License

This project is open-source and available under the MIT License.

Enjoy managing your personal library! 📚
