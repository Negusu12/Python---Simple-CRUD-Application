import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox

def start_application(parent_frame):
    # Clear the parent frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Create a new frame for this page
    frame = tk.Frame(parent_frame, bg='#ecf0f1')
    frame.pack(expand=True, fill='both')

    # Add a title label
    title_label = tk.Label(frame, text="Asset Record Management", font=('Arial', 24), bg='#ecf0f1', fg='#2c3e50')
    title_label.pack(pady=20)

    # Create a form for asset details
    form_frame = tk.Frame(frame, bg='#ecf0f1')
    form_frame.pack(pady=10)

    labels = ["Asset ID:", "Asset Name:", "Asset Type:", "Purchase Date:", "Cost:", "Location:"]
    global asset_id, asset_name, asset_type, purchase_date, cost, location

    # Create global variables for asset details
    asset_id = tk.StringVar()
    asset_name = tk.StringVar()
    asset_type = tk.StringVar()
    purchase_date = tk.StringVar()
    cost = tk.StringVar()
    location = tk.StringVar()

    for idx, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=('Arial', 16), bg='#ecf0f1').grid(row=idx, column=0, sticky='e', padx=10, pady=5)
        entry = tk.Entry(form_frame, textvariable=[asset_id, asset_name, asset_type, purchase_date, cost, location][idx], width=30)
        entry.grid(row=idx, column=1, padx=10, pady=5)

    # Add buttons for actions
    button_frame = tk.Frame(frame, bg='#ecf0f1')
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Add Asset", command=add_asset, bg='#3498db', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    tk.Button(button_frame, text="Update Asset", command=update_asset, bg='#3498db', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    tk.Button(button_frame, text="Delete Asset", command=delete_asset, bg='#e74c3c', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    tk.Button(button_frame, text="Back to Home", command=lambda: load_page("Home"), bg='#3498db', fg='white', font=('Arial', 12)).pack(side='left', padx=10)

    # Add a Treeview for displaying assets
    global tree
    columns = ("Asset ID", "Asset Name", "Asset Type", "Purchase Date", "Cost", "Location")
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    tree.pack(pady=20, fill='both', expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Bind the Treeview selection event
    tree.bind('<<TreeviewSelect>>', populate_fields)

    # Load initial data
    load_assets()

def add_asset():
    if any(not var.get() for var in [asset_id, asset_name, asset_type, purchase_date, cost, location]):
        tkMessageBox.showerror("Error", "Please complete all fields")
        return

    # Implement the actual database insertion logic here
    # Example:
    # conn = mysql.connector.connect(...)
    # cursor = conn.cursor()
    # cursor.execute(...)
    # conn.commit()
    # conn.close()

    # Update the Treeview
    load_assets()

    tkMessageBox.showinfo("Success", "Asset added successfully!")

def update_asset():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select an asset to update")
        return

    # Implement the actual database update logic here
    # Example:
    # conn = mysql.connector.connect(...)
    # cursor = conn.cursor()
    # cursor.execute(...)
    # conn.commit()
    # conn.close()

    # Update the Treeview
    load_assets()

    tkMessageBox.showinfo("Success", "Asset updated successfully!")

def delete_asset():
    selected_item = tree.selection()
    if not selected_item:
        tkMessageBox.showerror("Error", "Please select an asset to delete")
        return

    # Implement the actual database delete logic here
    # Example:
    # conn = mysql.connector.connect(...)
    # cursor = conn.cursor()
    # cursor.execute(...)
    # conn.commit()
    # conn.close()

    # Update the Treeview
    load_assets()

    tkMessageBox.showinfo("Success", "Asset deleted successfully!")

def load_assets():
    # Clear the Treeview
    tree.delete(*tree.get_children())

    # Implement the actual database retrieval logic here
    # Example:
    # conn = mysql.connector.connect(...)
    # cursor = conn.cursor()
    # cursor.execute(...)
    # data = cursor.fetchall()
    # conn.close()

    # Example data
    data = [
        ("1", "Laptop", "Electronics", "2023-01-15", "1000", "Office"),
        ("2", "Projector", "Electronics", "2022-11-10", "500", "Meeting Room")
    ]

    for item in data:
        tree.insert('', 'end', values=item)

def populate_fields(event):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)['values']
        asset_id.set(values[0])
        asset_name.set(values[1])
        asset_type.set(values[2])
        purchase_date.set(values[3])
        cost.set(values[4])
        location.set(values[5])

def load_page(page_name):
    # Function to handle page loading, will be defined in home.py
    pass
