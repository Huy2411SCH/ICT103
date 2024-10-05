import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3
import pandas as pd

class LoginSystem:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn1 = sqlite3.connect(self.db_path)
        self.cursor = self.conn1.cursor()
        self.create_user_table()
    def create_user_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
        )
        ''')
        self.conn1.commit()
   

    def add_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn1.commit()
            return "User added successfully!"
        except sqlite3.IntegrityError:
            return "Username already exists!"
    def login(self, username, password):
        
            self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',(username, password ))
            self.result= self.cursor.fetchone()

            return self.result

class BookSystem:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn2 = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_user_table()
    def create_user_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL)
        )
        ''')
        self.conn2.commit()

class MainWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login UI")
        #window.iconbitmap('./assets/pythontutorial.ico')
        self.window_width = 500
        self.window_height = 300 
        self.root.resizable = (True, True)
        self.root.minsize(500,300)
        self.root.maxsize(1920,1080)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.center_x = int(self.screen_width/2 - self.window_width / 2)
        self.center_y = int(self.screen_height/2 - self.window_height / 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.center_x}+{self.center_y}')
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
        self.add_button = ttk.Button(self.add_frame, text="Add Book", command=self.add_book)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWin(root)
    LoginSys = LoginSystem(r'C:\Users\skyhu\Documents\Labs\test.db')
    root.mainloop()