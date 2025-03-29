-- CREATE
INSERT INTO Books VALUES (3, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'Available');

-- READ
SELECT * FROM Books;

-- UPDATE
UPDATE Books SET availability_status = 'Borrowed' WHERE book_id = 1;

-- DELETE
DELETE FROM Borrowers WHERE borrower_id = 2;

-- JOIN
SELECT b.title, br.borrow_date, br.return_date, bw.name
FROM Books b
JOIN Borrow_Records br ON b.book_id = br.book_id
JOIN Borrowers bw ON br.borrower_id = bw.borrower_id;

-- SUBQUERY
SELECT title FROM Books
WHERE book_id NOT IN (SELECT book_id FROM Borrow_Records);
