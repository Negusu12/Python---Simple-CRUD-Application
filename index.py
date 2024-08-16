from tkinter import *
import mysql.connector
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from bcrypt import hashpw, gensalt, checkpw

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
    Top = Frame(parent_frame, width=1360, height=50, bd=8, relief="raise")
    Top.pack(side=TOP)
    Left = Frame(parent_frame, width=300, height=500, bd=8, relief="raise")
    Left.pack(side=LEFT)
    Right = Frame(parent_frame, width=760, height=500, bd=8, relief="raise")
    Right.pack(side=RIGHT)
    Forms = Frame(Left, width=300, height=450)
    Forms.pack(side=TOP)
    Buttons = Frame(Left, width=300, height=100, bd=8, relief="raise")
    Buttons.pack(side=BOTTOM)
    RadioGroup = Frame(Forms)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 16)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 16)).pack(side=LEFT)

     # ================================== LABEL WIDGET ========================================
    txt_title = Label(Top, width=900, font=('arial', 24), text="Python: Simple CRUD Application")
    txt_title.pack()
    txt_firstname = Label(Forms, text="Firstname:", font=('arial', 16), bd=15)
    txt_firstname.grid(row=0, stick="e")
    txt_lastname = Label(Forms, text="Lastname:", font=('arial', 16), bd=15)
    txt_lastname.grid(row=1, stick="e")
    txt_gender = Label(Forms, text="Gender:", font=('arial', 16), bd=15)
    txt_gender.grid(row=2, stick="e")
    txt_address = Label(Forms, text="Address:", font=('arial', 16), bd=15)
    txt_address.grid(row=3, stick="e")
    txt_username = Label(Forms, text="Username:", font=('arial', 16), bd=15)
    txt_username.grid(row=4, stick="e")
    txt_password = Label(Forms, text="Password:", font=('arial', 16), bd=15)
    txt_password.grid(row=5, stick="e")
    txt_result = Label(Buttons)
    txt_result.pack(side=TOP)

    # ================================== ENTRY WIDGET ========================================
    firstname = Entry(Forms, textvariable=FIRSTNAME, width=30)
    firstname.grid(row=0, column=1)
    lastname = Entry(Forms, textvariable=LASTNAME, width=30)
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    address = Entry(Forms, textvariable=ADDRESS, width=30)
    address.grid(row=3, column=1)
    username = Entry(Forms, textvariable=USERNAME, width=30)
    username.grid(row=4, column=1)
    password = Entry(Forms, textvariable=PASSWORD, show="*", width=30)
    password.grid(row=5, column=1)

    # ================================== BUTTONS WIDGET ======================================
    btn_create = Button(Buttons, width=10, text="Create", command=Create)
    btn_create.pack(side=LEFT)
    btn_read = Button(Buttons, width=10, text="Read", command=Read)
    btn_read.pack(side=LEFT)
    btn_update = Button(Buttons, width=10, text="Update", command=Update)
    btn_update.pack(side=LEFT)
    btn_delete = Button(Buttons, width=10, text="Delete", command=Delete)
    btn_delete.pack(side=LEFT)
    btn_exit = Button(Buttons, width=10, text="Exit", command=Exit)
    btn_exit.pack(side=LEFT)

    # ================================== LIST WIDGET =========================================
    scrollbary = Scrollbar(Right, orient=VERTICAL)
    scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
    tree = ttk.Treeview(Right, columns=("Firstname", "Lastname", "Gender", "Address", "Username", "Password"),
                        selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Firstname', text="Firstname", anchor=W)
    tree.heading('Lastname', text="Lastname", anchor=W)
    tree.heading('Gender', text="Gender", anchor=W)
    tree.heading('Address', text="Address", anchor=W)
    tree.heading('Username', text="Username", anchor=W)
    tree.heading('Password', text="Password", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=80)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=150)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.pack()

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
        txt_result.config(text="Please complete the required field!", fg="red")
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
        txt_result.config(text="Created a data!", fg="green")
        Read()

def Update():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select a record to update")
        return

    old_username = tree.item(selected_item)['values'][4]

    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or USERNAME.get() == "" or PASSWORD.get() == "":
        txt_result.config(text="Please complete the required field!", fg="red")
        return

    try:
        Database()
        hashed_password = hash_password(PASSWORD.get())

        cursor.execute(
            "UPDATE member SET firstname=%s, lastname=%s, gender=%s, address=%s, username=%s, password=%s WHERE username=%s",
            (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), ADDRESS.get(), USERNAME.get(), hashed_password,
             old_username))

        conn.commit()

        # Update the treeview item
        tree.item(selected_item,
                  values=(FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), ADDRESS.get(), USERNAME.get(), PASSWORD.get()))

        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")

        cursor.close()
        conn.close()
        txt_result.config(text="Record updated successfully!", fg="green")

    except mysql.connector.Error as err:
        txt_result.config(text=f"Error: {err}", fg="red")
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
    txt_result.config(text="Record deleted successfully!", fg="red")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    txt_result.config(text="Successfully read the data from database", fg="black")

def PopulateFields(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        FIRSTNAME.set(values[0])
        LASTNAME.set(values[1])
        GENDER.set(values[2])
        ADDRESS.set(values[3])
        USERNAME.set(values[4])
        PASSWORD.set("")  # Do not display password in the field

def Exit():
    result = tkMessageBox.askquestion('Python: Simple CRUD Application', 'Are you sure you want to exit?',
                                      icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

# Ensure this function is only run when the script is executed directly
if __name__ == '__main__':
    start_application(Tk())
