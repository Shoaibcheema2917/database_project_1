import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    availability_status TEXT
)""")
conn.commit()

def add_book():
    cursor.execute("INSERT INTO Books (title, author, genre, availability_status) VALUES (?, ?, ?, ?)",
                   (title_entry.get(), author_entry.get(), genre_entry.get(), status_entry.get()))
    conn.commit()
    messagebox.showinfo("Success", "Book added!")

def view_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    output.delete(1.0, tk.END)
    for book in books:
        output.insert(tk.END, str(book) + "\n")

def delete_book():
    cursor.execute("DELETE FROM Books WHERE book_id=?", (delete_entry.get(),))
    conn.commit()
    messagebox.showinfo("Deleted", "Book deleted!")

root = tk.Tk()
root.title("Library CRUD App")

tk.Label(root, text="Title").grid(row=0, column=0)
tk.Label(root, text="Author").grid(row=1, column=0)
tk.Label(root, text="Genre").grid(row=2, column=0)
tk.Label(root, text="Status").grid(row=3, column=0)

title_entry = tk.Entry(root)
author_entry = tk.Entry(root)
genre_entry = tk.Entry(root)
status_entry = tk.Entry(root)

title_entry.grid(row=0, column=1)
author_entry.grid(row=1, column=1)
genre_entry.grid(row=2, column=1)
status_entry.grid(row=3, column=1)

tk.Button(root, text="Add Book", command=add_book).grid(row=4, column=0, columnspan=2)
tk.Label(root, text="Book ID to Delete").grid(row=5, column=0)
delete_entry = tk.Entry(root)
delete_entry.grid(row=5, column=1)
tk.Button(root, text="Delete Book", command=delete_book).grid(row=6, column=0, columnspan=2)
tk.Button(root, text="View All Books", command=view_books).grid(row=7, column=0, columnspan=2)

output = tk.Text(root, height=10, width=50)
output.grid(row=8, column=0, columnspan=2)

root.mainloop()
