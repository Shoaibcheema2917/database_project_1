CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    availability_status TEXT
);

CREATE TABLE Borrowers (
    borrower_id INTEGER PRIMARY KEY,
    name TEXT,
    phone_number TEXT,
    email TEXT
);

CREATE TABLE Borrow_Records (
    record_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    borrower_id INTEGER,
    borrow_date TEXT,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);

CREATE TABLE Staff (
    staff_id INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    email TEXT
);
