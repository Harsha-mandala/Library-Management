# Library Management System

A simple, user-friendly **Library Management System** built with Python and Tkinter, using SQLite for data storage. This desktop application allows you to manage a library's book inventory, including adding, updating, deleting, and viewing book records, as well as tracking book issuance and returns.

## Features

- **Add New Books:** Enter book details and add them to the library database.
- **Update Book Details:** Modify existing book information.
- **Delete Book Records:** Remove individual books or clear the entire inventory.
- **Issue & Return Books:** Track the status of each book (Available/Issued) and record the issuer's card ID.
- **View Inventory:** Browse all books in a sortable, scrollable table.
- **Modern UI:** Clean, pastel-themed interface with improved fonts and button styles.

## Technologies Used

| Component   | Technology         |
|-------------|-------------------|
| Language    | Python 3.x        |
| GUI         | Tkinter           |
| Database    | SQLite (via sqlite3 module) |

## Getting Started

### Prerequisites

- Python 3.x installed on your system (Tkinter and sqlite3 are included by default).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Run the application:**
   ```bash
   python library_management.py
   ```

   *(No additional dependencies required.)*

## Usage

- **Add Record:** Fill in the book details and click "Add Record".
- **Update Details:** Select a book from the table, edit the fields, and click "Update Details".
- **Delete Record:** Select a book and click "Delete Record".
- **Delete All:** Remove all books from the inventory.
- **Change Status:** Issue or return a book by changing its status.
- **Clear Fields:** Reset all input fields.

## Screenshots

*(Add screenshots of your application here to showcase the interface and features.)*

## Customization

- **Colors and Fonts:** Easily modify the color scheme and fonts in the script to match your preferences.
- **Database:** The application uses a local `library.db` SQLite database file for storage.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements

- Built using Python's standard libraries for maximum compatibility and ease of use.
- Inspired by classic library management workflows and modern UI design principles.

**Feel free to fork, modify, and contribute to this project!**
