# Personal Library Manager

Welcome to the **Personal Library Manager**! This is a simple command-line application that helps you manage your personal library of books. You can add, remove, search, and display books, as well as view statistics about your library. The application uses an SQLite database to store all the book information.

---

## Features

- **Add a Book**: Add a new book to your library by providing details like title, author, publication year, genre, content, and read status.
- **Remove a Book**: Remove a book from your library using its unique ID.
- **Search for a Book**: Search for a book by its title, author, or ID.
- **Display All Books**: View a list of all the books in your library.
- **Library Statistics**: View statistics like the total number of books and the percentage of books you've read.

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
   - Steps:
     1. Enter the title of the book.
     2. Enter the author of the book.
     3. Enter the publication year of the book.
     4. Enter the genre of the book.
     5. Enter the content or description of the book.
     6. Specify whether you've read the book (yes/no).
   - Example:
     ```bash
     python library_manager.py add
     ```

### 2. **Remove a Book**
   - Command: `python library_manager.py remove`
   - Description: Remove a book from your library using its unique ID.
   - Steps:
     1. Enter the ID of the book you want to remove.
   - Example:
     ```bash
     python library_manager.py remove
     ```

### 3. **Search for a Book**
   - Command: `python library_manager.py search`
   - Description: Search for a book by its title, author, or ID.
   - Steps:
     1. Enter the title, author, or ID of the book you want to search for.
   - Example:
     ```bash
     python library_manager.py search
     ```

### 4. **Display All Books**
   - Command: `python library_manager.py display`
   - Description: Display a list of all the books in your library.
   - Example:
     ```bash
     python library_manager.py display
     ```

### 5. **View Library Statistics**
   - Command: `python library_manager.py stats`
   - Description: View statistics about your library, such as the total number of books and the percentage of books you've read.
   - Example:
     ```bash
     python library_manager.py stats
     ```

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

## Steps to Create the Database (For Beginners)

If you're new to databases, don't worry! Here's a step-by-step guide to understanding how the database works in this project:

1. **What is a Database?**
   - A database is like a digital filing cabinet where you can store and organize data.
   - In this project, the database stores information about your books.

2. **What is SQLite?**
   - SQLite is a simple, file-based database system.
   - It doesn't require any setup or installation because it's included with Python.

3. **How is the Database Created?**
   - When you run the script, the `init_database()` function is executed.
   - This function creates a file named `library.db` (if it doesn't exist) and sets up the `books` table.

4. **How is Data Stored?**
   - Each book is stored as a row in the `books` table.
   - The columns in the table represent different attributes of the book (e.g., title, author, year).

5. **How is Data Retrieved?**
   - When you search for a book or display all books, the script queries the database to retrieve the relevant data.

---

## Example Workflow

1. **Add a Book**:
   ```bash
   python library_manager.py add
   ```
   Enter the book details when prompted.

2. **Display All Books**:
   ```bash
   python library_manager.py display
   ```
   View the list of all books in your library.

3. **Search for a Book**:
   ```bash
   python library_manager.py search
   ```
   Search for a book by title, author, or ID.

4. **Remove a Book**:
   ```bash
   python library_manager.py remove
   ```
   Remove a book by entering its ID.

5. **View Statistics**:
   ```bash
   python library_manager.py stats
   ```
   View the total number of books and the percentage of books you've read.

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
