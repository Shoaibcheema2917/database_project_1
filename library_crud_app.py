import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)

# --- Database Setup ---
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    availability_status TEXT NOT NULL
)""")
conn.commit()

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library CRUD App (PyQt5)")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()

    def init_ui(self):
        # --- Form Layout for Inputs ---
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QLineEdit()

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("Genre:", self.genre_input)
        form_layout.addRow("Status:", self.status_input)

        # --- Buttons ---
        self.add_btn = QPushButton("Add Book")
        self.add_btn.clicked.connect(self.add_book)

        self.delete_id_input = QLineEdit()
        form_layout.addRow("Book ID to Delete:", self.delete_id_input)

        self.delete_btn = QPushButton("Delete Book")
        self.delete_btn.clicked.connect(self.delete_book)

        self.view_btn = QPushButton("View All Books")
        self.view_btn.clicked.connect(self.view_books)

        # --- Output Area ---
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # --- Layout Composition ---
        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)

        hbox = QHBoxLayout()
        hbox.addWidget(self.add_btn)
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.view_btn)
        vbox.addLayout(hbox)

        vbox.addWidget(QLabel("Library Records:"))
        vbox.addWidget(self.output)

        self.setLayout(vbox)

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        genre = self.genre_input.text().strip()
        status = self.status_input.text().strip()

        if not (title and author and genre and status):
            QMessageBox.critical(self, "Input Error", "All fields are required.")
            return

        cursor.execute("INSERT INTO Books (title, author, genre, availability_status) VALUES (?, ?, ?, ?)",
                       (title, author, genre, status))
        conn.commit()
        QMessageBox.information(self, "Success", "Book added successfully.")
        self.clear_inputs()

    def view_books(self):
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        self.output.clear()
        if books:
            for book in books:
                self.output.append(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}")
        else:
            self.output.append("No books found.")

    def delete_book(self):
        book_id = self.delete_id_input.text().strip()
        if not book_id.isdigit():
            QMessageBox.critical(self, "Input Error", "Please enter a valid numeric Book ID.")
            return

        cursor.execute("SELECT * FROM Books WHERE book_id=?", (book_id,))
        if cursor.fetchone() is None:
            QMessageBox.warning(self, "Not Found", f"No book found with ID {book_id}.")
            return

        cursor.execute("DELETE FROM Books WHERE book_id=?", (book_id,))
        conn.commit()
        QMessageBox.information(self, "Deleted", f"Book with ID {book_id} deleted.")
        self.delete_id_input.clear()

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.genre_input.clear()
        self.status_input.clear()

    def closeEvent(self, event):
        conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())