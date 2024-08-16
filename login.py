from tkinter import *
import mysql.connector
import tkinter.messagebox as tkMessageBox
from bcrypt import checkpw
import index  # Import the index module

def login(event=None):  # Accept an event parameter for key binding
    username = username_var.get()
    password = password_var.get()

    if username == "" or password == "":
        tkMessageBox.showerror("Error", "Please enter both username and password")
        return

    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='pythontut'
    )
    cursor = conn.cursor()

    # Fetch user from database
    cursor.execute("SELECT password FROM member WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        # Convert the password from the database to bytes if it's stored as a string
        hashed_password = result[0]
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')

        if checkpw(password.encode('utf-8'), hashed_password):
            root.destroy()  # Hide the login window
            index.start_application()  # Show the main application window from index.py
        else:
            tkMessageBox.showerror("Error", "Invalid username or password")
    else:
        tkMessageBox.showerror("Error", "Invalid username or password")

    cursor.close()
    conn.close()

# Create the login window
root = Tk()
root.title("Login")

# Initialize StringVar variables
username_var = StringVar()
password_var = StringVar()

# Set the dimensions of the window
root.geometry("1360x760")
root.resizable(False, False)

# Center the window on the screen
window_width = 1360
window_height = 760
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) / 2
y = (screen_height - window_height) / 2
root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

# Style the login window
root.configure(bg='#f0f0f0')

# Create and style frames
frame = Frame(root, bg='#ffffff', padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(frame, text="Username", bg='#ffffff', font=('Arial', 12)).pack(pady=5)
username_entry = Entry(frame, textvariable=username_var, width=25, font=('Arial', 12))
username_entry.pack(pady=5)

Label(frame, text="Password", bg='#ffffff', font=('Arial', 12)).pack(pady=5)
password_entry = Entry(frame, textvariable=password_var, show="*", width=25, font=('Arial', 12))
password_entry.pack(pady=5)

Button(frame, text="Login", command=login, bg='#4CAF50', fg='white', font=('Arial', 12), padx=10, pady=5).pack(pady=10)

# Bind the Enter key to the login function
root.bind('<Return>', login)

# Optionally, add a logo or additional styling
# logo = PhotoImage(file="logo.png")  # Uncomment if you have a logo
# Label(frame, image=logo, bg='#ffffff').pack(pady=10)

root.mainloop()