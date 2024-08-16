import tkinter as tk
from tkinter import ttk
import index
import asset_record

def load_index():
    # Clear the main content area
    for widget in main_area.winfo_children():
        widget.destroy()
    
    # Load the index content into the main_area
    index.start_application(main_area)

def load_page(page_name):
    if page_name == "Index":
        load_index()
    # Add more conditions here for other pages
    # elif page_name == "AnotherPage":
    #     load_another_page()


def load_asset_record():
    # Clear the main content area
    for widget in main_area.winfo_children():
        widget.destroy()
    asset_record.start_application(main_area)

def load_page(page_name):
    if page_name == "Asset_record":
        load_asset_record()



# Create the main window
root = tk.Tk()
root.title("Home Page")

# Set the dimensions of the window
root.geometry("1360x760")
root.resizable(False, False)

# Style the main window
root.configure(bg='#f0f0f0')

# Create the sidebar frame
sidebar = tk.Frame(root, width=200, bg='#2c3e50', height=600, relief='raised', padx=40)
sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

# Create the main content area frame
main_area = tk.Frame(root, bg='#ecf0f1', width=600, height=600)
main_area.pack(expand=True, fill='both', side='right')

# Add buttons to the sidebar for navigation
buttons = [
    ("Index", load_index),
    ("Asset_record", load_asset_record),
    # Add more buttons here for other pages
    # ("AnotherPage", lambda: load_page("AnotherPage"))
]

for text, command in buttons:
    button = tk.Button(sidebar, text=text, command=command, bg='#34495e', fg='white', font=('Arial', 12), bd=0, pady=10)
    button.pack(fill='x', pady=5)

# Add a label in the main content area as a placeholder
main_label = tk.Label(main_area, text="Welcome to the Home Page", font=('Arial', 24), bg='#ecf0f1', fg='#2c3e50')
main_label.pack(pady=200)

# Start the main loop
root.mainloop()
