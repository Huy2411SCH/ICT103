import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

window = tk.Tk()
window.title("Hello World")
#window.iconbitmap('./assets/pythontutorial.ico')
window_width = 500
window_height = 300
# the ability to resize
window.resizable(True, True)
window.minsize(500, 300)
window.maxsize(1920, 1080)
# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


# Sign in frame
signin = ttk.Frame(window)
signin.pack(padx=10, pady=10, fill='x', expand=True)

# store email address and password
email = tk.StringVar()
password = tk.StringVar()
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class LoginSystem:
    def __init__(self):
        self.users = []

    def register(self, username, password):
        user = User(username, password)
        self.users.append(user)
        print(f"User {username} registered successfully!")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                print(f"Welcome, {username}!")
                return True
        print("Invalid username or password.")
        return False

def login_clicked():
    """ callback when the login button clicked
    """
    msg = f'You entered email: {email.get()} and password: {password.get()}'
    showinfo(
        title='Information',
        message=msg
    )
LoginSys = LoginSystem()
def register_clicked():
    LoginSys.register(email.get(),password.get())

# email
email_label = ttk.Label(signin, text="Email Address:")
email_label.pack(fill='x',padx=100, pady=0, expand=True)

email_entry = ttk.Entry(signin, textvariable=email)
email_entry.pack(fill='x',padx=100, pady=0, expand=True)

email_entry.focus()

# password
password_label = ttk.Label(signin, text="Password:")
password_label.pack(fill='x',padx=100, pady=0, expand=True)

password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.pack(fill='x',padx=100, pady=0, expand=True)

# login button
login_button = ttk.Button(signin, text="Login", command=login_clicked)
login_button.pack(fill='x',padx=100, pady=10, expand=True, )
# login button
register_button = ttk.Button(signin, text="Register", command=register_clicked)
register_button.pack(fill='x',padx=100, pady=10, expand=True, )


# keep the window on
window.mainloop()