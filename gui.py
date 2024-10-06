import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3
import pandas as pd

class LoginSystem:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn1 = sqlite3.connect(self.db_path) # connect to database
        self.cursor = self.conn1.cursor()
        self.create_user_table()
    def create_user_table(self): # create account database if not exists
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
        )
        ''')
        self.conn1.commit()
   

    def add_user(self, username, password): # add user details into database
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn1.commit()
            return "User added successfully!"
        except sqlite3.IntegrityError:
            return "Username already exists!"
    def login(self, username, password):  # check if login details are correct
        
            self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',(username, password ))
            self.result= self.cursor.fetchone()

            return self.result

class BookSystem:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn2 = sqlite3.connect(self.db_path) # connect to database
        self.cursor = self.conn2.cursor()
        self.create_user_table()
    def create_user_table(self): # create database if not exists
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL)
        
        ''')
        self.conn2.commit()
    def add_book(self,title,author,year): # add book to database
            cursor = self.conn2.cursor()
            cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
            self.conn2.commit()
    def search_books(self,search_term):
        cursor = self.conn2.cursor()
        cursor.execute('''
            SELECT * FROM books 
            WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR CAST(year AS TEXT) LIKE ?
        ''', ('%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%'))
        return cursor.fetchall()
    def delete_book(self,book_id):
        cursor = self.conn2.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn2.commit()
    def book_list(self): #receive all books from database
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        return books

class MainWin:
    def __init__(self, root):
        self.root = root
        
        #title
        self.root.title("Library")
        
        # icon
        self.root.iconbitmap('./book.ico')

        #set size
        self.window_width = 500
        self.window_height = 300

        # the ability to resize
        self.root.resizable = (True, True)
        self.root.minsize(500,300)
        self.root.maxsize(1920,1080)

        # get the screen dimension
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # find the center point
        self.center_x = int(self.screen_width/2 - self.window_width / 2)
        self.center_y = int(self.screen_height/2 - self.window_height / 2)

        # set the position of the window to the center of the screen
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')
        
        #store email, password to variables
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.create_login_frame()
    def create_login_frame(self):
        # Sign in frame
        self.signin = ttk.Frame(self.root)
        self.signin.pack(padx=10, pady=10, fill='x', expand=True)
        
        # email
        self.email_label = ttk.Label(self.signin, text="Email Address:")
        self.email_label.pack(fill='x',padx=100, pady=0, expand=True)

        self.email_entry = ttk.Entry(self.signin, textvariable=self.email)
        self.email_entry.pack(fill='x',padx=100, pady=0, expand=True)

        self.email_entry.focus()

        # password
        self.password_label = ttk.Label(self.signin, text="Password:")
        self.password_label.pack(fill='x',padx=100, pady=0, expand=True)

        self.password_entry = ttk.Entry(self.signin, textvariable=self.password, show="*")
        self.password_entry.pack(fill='x',padx=100, pady=0, expand=True)

            # login button
        self.login_button = ttk.Button(self.signin, text="Login", command=self.login_clicked)
        self.login_button.pack(fill='x',padx=100, pady=10, expand=True, )
        # login button
        self.register_button = ttk.Button(self.signin, text="Register",command=self.register_clicked)
        self.register_button.pack(fill='x',padx=100, pady=10, expand=True, )
    def login_clicked(self):
        if LoginSys.login(self.email.get(),self.password.get()):
            self.hide_signin_frame()
            self.create_books_system()
            msg = 'You have logged in'
            showinfo(
                title='Information',
                message=msg)
        else:
            msg = 'Incorrect email or password'
            showinfo(
                title='Information',
                message=msg)
    def register_clicked(self):
            msg = LoginSys.add_user(self.email.get(),self.password.get())
            showinfo(
                title='Information',
                message=msg)    
    def hide_signin_frame(self):
         self.signin.pack_forget()
    def create_books_system(self):
                 # Create and set up the notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create frames
        self.add_frame = ttk.Frame(self.notebook)
        self.view_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.add_frame, text="Add Book")
        self.notebook.add(self.view_frame, text="View Books")
        self.notebook.add(self.search_frame, text="Search Books")
        self.setup_add_book_frame()
        self.setup_view_books_frame()
        self.setup_search_books_frame()

    def setup_add_book_frame(self):
        # Title
        ttk.Label(self.add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Author
        ttk.Label(self.add_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(self.add_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        # Year
        ttk.Label(self.add_frame, text="Year:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(self.add_frame, width=40)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        # Add Book Button
        self.add_button = ttk.Button(self.add_frame, text="Add Book", command=self.ui_add_book)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)
    def setup_view_books_frame(self):
        # Create Treeview
        self.tree = ttk.Treeview(self.view_frame, columns=('ID', 'Title', 'Author', 'Year'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Author', text='Author')
        self.tree.heading('Year', text='Year')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Delete Book Button
        self.delete_button = ttk.Button(self.view_frame, text="Delete Selected", command=self.ui_delete_book)
        self.delete_button.pack(pady=10)

        # Refresh Button
        self.refresh_button = ttk.Button(self.view_frame, text="Refresh", command=self.refresh_book_list)
        self.refresh_button.pack(pady=10)

        # Load books
        self.refresh_book_list()

    def setup_search_books_frame(self):
        # Search entry
        ttk.Label(self.search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Search button
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.ui_search_books)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Search results
        self.search_results = ttk.Treeview(self.search_frame, columns=('ID', 'Title', 'Author', 'Year'), show='headings')
        self.search_results.heading('ID', text='ID')
        self.search_results.heading('Title', text='Title')
        self.search_results.heading('Author', text='Author')
        self.search_results.heading('Year', text='Year')
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Configure grid weights
        self.search_frame.grid_rowconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=1)
    def ui_add_book(self):
        
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        if title and author and year:   #require user to fill all the fields
            print("added")
            BookSys.add_book(title,author,year)
            self.clear_entries()
        else:
            msg = 'Please fill in every fields'
            showinfo(
                title='Error',
                message=msg)
    def ui_search_books(self):
        search_term = self.search_entry.get().lower()
        
        # Clear previous search results
        for item in self.search_results.get_children():
            self.search_results.delete(item)

        # Search and display results
        results = BookSys.search_books(search_term)
        
        for book in results:
            self.search_results.insert('', tk.END, values=book)

        if not self.search_results.get_children():
            msg = "No matching books found."
            showinfo(
                title='Search Results',
                message=msg)
    def ui_delete_book(self):
        selected_item = self.tree.selection()
        if selected_item:
            book_id = self.tree.item(selected_item)['values'][0]
            BookSys.delete_book(book_id)
            self.refresh_book_list()
            msg = "Deleted successfully"
            showinfo(
                title='',
                message=msg)
        else:
            msg = "Please select a book"
            showinfo(
                title='Error',
                message=msg)
    def refresh_book_list(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert books into the treeview
        for book in BookSys.book_list():
            self.tree.insert('', tk.END, values=book)
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWin(root)
    LoginSys = LoginSystem(r'C:\Users\skyhu\Documents\Labs\test.db')
    BookSys = BookSystem(r'C:\Users\skyhu\Documents\Labs\books.db')
    root.mainloop()
  
