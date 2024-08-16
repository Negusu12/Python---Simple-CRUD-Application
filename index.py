from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import mysql.connector
from bcrypt import hashpw, gensalt

def start_application(parent_frame):
    global FIRSTNAME, LASTNAME, GENDER, ADDRESS, USERNAME, PASSWORD
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    GENDER = StringVar()
    ADDRESS = StringVar()
    USERNAME = StringVar()
    PASSWORD = StringVar()

    # ================================== FRAME ===============================================
    global tree, txt_result
    Top = ttk.Frame(parent_frame, padding=10)
    Top.pack(side=TOP, fill=X)
    Left = ttk.Frame(parent_frame, padding=10)
    Left.pack(side=LEFT, fill=Y)
    Right = ttk.Frame(parent_frame, padding=10)
    Right.pack(side=RIGHT, fill=BOTH, expand=True)

    Forms = ttk.Frame(Left, padding=10)
    Forms.pack(side=TOP, fill=BOTH, expand=True)
    Buttons = ttk.Frame(Left, padding=10)
    Buttons.pack(side=BOTTOM, fill=X)

    RadioGroup = ttk.Frame(Forms)
    Male = ttk.Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male")
    Male.pack(side=LEFT)
    Female = ttk.Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female")
    Female.pack(side=LEFT)

    # ================================== LABEL WIDGET ========================================
    txt_title = ttk.Label(Top, text="Python: Simple CRUD Application", font=('arial', 24))
    txt_title.pack()
    labels = ["Firstname:", "Lastname:", "Gender:", "Address:", "Username:", "Password:"]
    for i, text in enumerate(labels):
        ttk.Label(Forms, text=text, font=('arial', 16)).grid(row=i, column=0, sticky="e", padx=10, pady=5)

    txt_result = ttk.Label(Buttons)
    txt_result.pack(side=TOP, fill=X)

    # ================================== ENTRY WIDGET ========================================
    ttk.Entry(Forms, textvariable=FIRSTNAME, width=30).grid(row=0, column=1, padx=10, pady=5)
    ttk.Entry(Forms, textvariable=LASTNAME, width=30).grid(row=1, column=1, padx=10, pady=5)
    RadioGroup.grid(row=2, column=1, padx=10, pady=5)
    ttk.Entry(Forms, textvariable=ADDRESS, width=30).grid(row=3, column=1, padx=10, pady=5)
    ttk.Entry(Forms, textvariable=USERNAME, width=30).grid(row=4, column=1, padx=10, pady=5)
    ttk.Entry(Forms, textvariable=PASSWORD, show="*", width=30).grid(row=5, column=1, padx=10, pady=5)

    # ================================== BUTTONS WIDGET ======================================
    ttk.Button(Buttons, text="Create", command=Create).pack(side=LEFT, padx=5)
    ttk.Button(Buttons, text="Read", command=Read).pack(side=LEFT, padx=5)
    ttk.Button(Buttons, text="Update", command=Update).pack(side=LEFT, padx=5)
    ttk.Button(Buttons, text="Delete", command=Delete).pack(side=LEFT, padx=5)
    ttk.Button(Buttons, text="Exit", command=Exit).pack(side=LEFT, padx=5)

    # ================================== LIST WIDGET =========================================
    scrollbary = ttk.Scrollbar(Right, orient=VERTICAL)
    scrollbarx = ttk.Scrollbar(Right, orient=HORIZONTAL)
    tree = ttk.Treeview(Right, columns=("Firstname", "Lastname", "Gender", "Address", "Username", "Password"),
                        selectmode="extended", height=25, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Firstname', text="Firstname")
    tree.heading('Lastname', text="Lastname")
    tree.heading('Gender', text="Gender")
    tree.heading('Address', text="Address")
    tree.heading('Username', text="Username")
    tree.heading('Password', text="Password")
    tree.column('#0', width=0, stretch=NO)
    tree.column('#1', width=100)
    tree.column('#2', width=120)
    tree.column('#3', width=80)
    tree.column('#4', width=150)
    tree.column('#5', width=120)
    tree.column('#6', width=120)
    tree.pack(fill=BOTH, expand=True)

    # Bind the Treeview selection event
    tree.bind('<<TreeviewSelect>>', PopulateFields)

    # ================================== INITIALIZATION ======================================
    Read()  # Initial read to populate the table
    root.mainloop()

# ============================= CRUD FUNCTIONS =============================

def Database():
    global conn, cursor
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='pythontut'
    )
    cursor = conn.cursor()

def hash_password(password):
    return hashpw(password.encode('utf-8'), gensalt())

def Create():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or USERNAME.get() == "" or PASSWORD.get() == "":
        tkMessageBox.showerror("Error", "Please complete the required field!")
    else:
        Database()
        hashed_password = hash_password(PASSWORD.get())
        cursor.execute(
            "INSERT INTO member (firstname, lastname, gender, address, username, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), ADDRESS.get(), USERNAME.get(), hashed_password))
        conn.commit()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")
        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Success", "Created a data!")
        Read()

def Update():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select a record to update")
        return

    old_username = tree.item(selected_item)['values'][4]

    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or USERNAME.get() == "" or PASSWORD.get() == "":
        tkMessageBox.showerror("Error", "Please complete the required field!")
        return

    try:
        Database()
        hashed_password = hash_password(PASSWORD.get())

        cursor.execute(
            "UPDATE member SET firstname=%s, lastname=%s, gender=%s, address=%s, username=%s, password=%s WHERE username=%s",
            (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), ADDRESS.get(), USERNAME.get(), hashed_password, old_username))

        conn.commit()

        # Update the treeview item
        tree.item(selected_item, values=(FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), ADDRESS.get(), USERNAME.get(), PASSWORD.get()))

        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")

        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Success", "Record updated successfully!")

    except mysql.connector.Error as err:
        tkMessageBox.showerror("Error", f"Error: {err}")
        print(f"Error: {err}")

def Delete():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select a record to delete")
        return

    username = tree.item(selected_item)['values'][4]
    Database()
    cursor.execute("DELETE FROM member WHERE username=%s", (username,))
    conn.commit()
    cursor.close()
    conn.close()
    Read()  # Refresh the list
    tkMessageBox.showinfo("Success", "Record deleted successfully!")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()

def PopulateFields(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        FIRSTNAME.set(values[0])
        LASTNAME.set(values[1])
        GENDER.set(values[2])
        ADDRESS.set(values[3])
        USERNAME.set(values[4])
        PASSWORD.set("")  # Do not display the password in the field

def Exit():
    result = tkMessageBox.askquestion('Confirm Exit', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

# Ensure this function is only run when the script is executed directly
if __name__ == '__main__':
    root = Tk()
    root.title("Python CRUD Application")
    root.geometry("1200x600")
    start_application(root)
