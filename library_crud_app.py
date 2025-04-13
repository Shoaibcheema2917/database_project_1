import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QTabWidget
)

# --- Database Setup ---
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# --- Setup Tables ---
cursor.executescript("""
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    availability_status TEXT
);

CREATE TABLE IF NOT EXISTS Borrowers (
    borrower_id INTEGER PRIMARY KEY,
    name TEXT,
    phone_number TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS Borrow_Records (
    record_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    borrower_id INTEGER,
    borrow_date TEXT,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);

CREATE TABLE IF NOT EXISTS Staff (
    staff_id INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    email TEXT
);
""")
conn.commit()

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 700, 600)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()

        self.tabs.addTab(self.books_tab(), "Books")
        self.tabs.addTab(self.borrowers_tab(), "Borrowers")
        self.tabs.addTab(self.records_tab(), "Borrow Records")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def books_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        form = QFormLayout()

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QLineEdit()

        form.addRow("Title:", self.title_input)
        form.addRow("Author:", self.author_input)
        form.addRow("Genre:", self.genre_input)
        form.addRow("Status:", self.status_input)

        self.add_book_btn = QPushButton("Add Book")
        self.add_book_btn.clicked.connect(self.add_book)

        self.books_output = QTextEdit()
        self.books_output.setReadOnly(True)

        self.view_books_btn = QPushButton("View Books")
        self.view_books_btn.clicked.connect(self.view_books)

        layout.addLayout(form)
        layout.addWidget(self.add_book_btn)
        layout.addWidget(self.view_books_btn)
        layout.addWidget(self.books_output)
        widget.setLayout(layout)
        return widget

    def borrowers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        form = QFormLayout()

        self.borrower_name = QLineEdit()
        self.borrower_phone = QLineEdit()
        self.borrower_email = QLineEdit()

        form.addRow("Name:", self.borrower_name)
        form.addRow("Phone:", self.borrower_phone)
        form.addRow("Email:", self.borrower_email)

        self.add_borrower_btn = QPushButton("Add Borrower")
        self.add_borrower_btn.clicked.connect(self.add_borrower)

        self.view_borrowers_btn = QPushButton("View Borrowers")
        self.view_borrowers_btn.clicked.connect(self.view_borrowers)

        self.borrowers_output = QTextEdit()
        self.borrowers_output.setReadOnly(True)

        layout.addLayout(form)
        layout.addWidget(self.add_borrower_btn)
        layout.addWidget(self.view_borrowers_btn)
        layout.addWidget(self.borrowers_output)
        widget.setLayout(layout)
        return widget

    def records_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        form = QFormLayout()

        self.record_book_id = QLineEdit()
        self.record_borrower_id = QLineEdit()
        self.record_borrow_date = QLineEdit()
        self.record_return_date = QLineEdit()

        form.addRow("Book ID:", self.record_book_id)
        form.addRow("Borrower ID:", self.record_borrower_id)
        form.addRow("Borrow Date:", self.record_borrow_date)
        form.addRow("Return Date:", self.record_return_date)

        self.add_record_btn = QPushButton("Add Record")
        self.add_record_btn.clicked.connect(self.add_record)

        self.view_records_btn = QPushButton("View Records")
        self.view_records_btn.clicked.connect(self.view_records)

        self.records_output = QTextEdit()
        self.records_output.setReadOnly(True)

        layout.addLayout(form)
        layout.addWidget(self.add_record_btn)
        layout.addWidget(self.view_records_btn)
        layout.addWidget(self.records_output)
        widget.setLayout(layout)
        return widget

    def add_book(self):
        data = (
            self.title_input.text(), self.author_input.text(),
            self.genre_input.text(), self.status_input.text()
        )
        cursor.execute("INSERT INTO Books (title, author, genre, availability_status) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        QMessageBox.information(self, "Success", "Book added successfully")

    def view_books(self):
        cursor.execute("SELECT * FROM Books")
        self.books_output.clear()
        for row in cursor.fetchall():
            self.books_output.append(str(row))

    def add_borrower(self):
        data = (
            self.borrower_name.text(),
            self.borrower_phone.text(),
            self.borrower_email.text()
        )
        cursor.execute("INSERT INTO Borrowers (name, phone_number, email) VALUES (?, ?, ?)", data)
        conn.commit()
        QMessageBox.information(self, "Success", "Borrower added successfully")

    def view_borrowers(self):
        cursor.execute("SELECT * FROM Borrowers")
        self.borrowers_output.clear()
        for row in cursor.fetchall():
            self.borrowers_output.append(str(row))

    def add_record(self):
        data = (
            self.record_book_id.text(),
            self.record_borrower_id.text(),
            self.record_borrow_date.text(),
            self.record_return_date.text()
        )
        cursor.execute("INSERT INTO Borrow_Records (book_id, borrower_id, borrow_date, return_date) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        QMessageBox.information(self, "Success", "Borrow record added")

    def view_records(self):
        cursor.execute('''SELECT b.title, br.borrow_date, br.return_date, bw.name
                          FROM Books b
                          JOIN Borrow_Records br ON b.book_id = br.book_id
                          JOIN Borrowers bw ON br.borrower_id = bw.borrower_id''')
        self.records_output.clear()
        for row in cursor.fetchall():
            self.records_output.append(f"Book: {row[0]}, Borrower: {row[3]}, Borrowed: {row[1]}, Returned: {row[2]}")

    def closeEvent(self, event):
        conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())