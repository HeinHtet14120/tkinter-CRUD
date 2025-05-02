import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from PIL import Image, ImageTk  # Add this import for handling images
import os
import csv
from product_types import PRODUCT_TYPES
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Create the main window
root = tb.Window(themename="darkly")  # or "superhero", "cyborg", etc.
root.title("Product Management System")
root.geometry("900x600")  # Set window size (width x height)

style = ttk.Style()
style.theme_use('clam')

# Dark colors
DARK_BG = "#23272e"
DARK_FG = "#f5f6fa"
DARK_ACCENT = "#4a90e2"
DARK_HEADER = "#1a1d23"
DARK_SELECT = "#357ab7"

# Set window background
root.configure(bg=DARK_BG)

# Table header style
style.configure("Treeview.Heading", 
                font=("Arial", 12, "bold"), 
                background=DARK_HEADER, 
                foreground=DARK_ACCENT)

# Table row style
style.configure("Treeview", 
                font=("Arial", 11),
                rowheight=28,
                background=DARK_BG,
                fieldbackground=DARK_BG,
                foreground=DARK_FG)

# Selected row color
style.map("Treeview", background=[('selected', DARK_SELECT)])

# Custom button style
style.configure("Custom.TButton",
                font=("Arial", 12, "bold"),
                foreground=DARK_FG,
                background=DARK_ACCENT,
                borderwidth=0,
                focusthickness=3,
                focuscolor='none',
                padding=8)
style.map("Custom.TButton",
          background=[('active', DARK_SELECT)])

# Entry and frame backgrounds
style.configure("TEntry", fieldbackground=DARK_HEADER, foreground=DARK_FG)
style.configure("TFrame", background=DARK_BG)
style.configure("TLabel", background=DARK_BG, foreground=DARK_FG)

# Combobox dark mode
style.map('TCombobox', fieldbackground=[('readonly', DARK_HEADER)],
          selectbackground=[('readonly', DARK_HEADER)],
          selectforeground=[('readonly', DARK_FG)])
style.configure('TCombobox', foreground=DARK_FG, background=DARK_HEADER)

# Search entry style
style.configure("Search.TEntry",
    foreground=DARK_FG,
    fieldbackground=DARK_HEADER,
    background=DARK_HEADER,
    bordercolor=DARK_ACCENT,
    lightcolor=DARK_ACCENT,
    darkcolor=DARK_HEADER,
    borderwidth=2,
    relief="flat",
    padding=8
)

# CSV file path
CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.csv')

# Create frames
# Logo frame for the logo
logo_frame = ttk.Frame(root, padding="10", style="TFrame")
logo_frame.pack(fill=tk.X)

# Load and display the logo
def load_logo():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, 'images', 'logo.png')
    
    try:
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found at {logo_path}")
            
        # Load the image using PIL
        logo_image = Image.open(logo_path)
        # Resize the image if needed (optional)
        logo_image = logo_image.resize((100, 100))  # Adjust size as needed
        # Convert PIL image to PhotoImage
        logo_photo = ImageTk.PhotoImage(logo_image)
        # Create label to display logo
        logo_label = ttk.Label(logo_frame, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference!
        logo_label.pack(side=tk.LEFT)
        return True
    except Exception as e:
        print(f"Could not load logo: {e}")
        return False

# Try to load the logo
if not load_logo():
    # If logo fails to load, show text instead
    backup_label = ttk.Label(logo_frame, text="PMS", 
                           font=("Helvetica", 24, "bold"))
    backup_label.pack(side=tk.LEFT)

# Add title next to logo
title_label = ttk.Label(logo_frame, text="Product Management System", 
                       font=("Helvetica", 16, "bold"))
title_label.pack(side=tk.LEFT, padx=20)

top_frame = ttk.Frame(root, padding="10", style="TFrame")
top_frame.pack(fill=tk.X)

main_frame = ttk.Frame(root, padding="10", style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a simple table structure using Treeview
columns = ('name', 'type', 'color', 'weight', 'price', 'brand')
tree = ttk.Treeview(main_frame, columns=columns, show='headings')

# Set up the columns
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)

# Add a scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack the tree and scrollbar
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def load_products():
    """Load products from CSV file and populate the table"""
    try:
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Read and populate from CSV
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tree.insert('', tk.END, values=(
                    row['name'], row['type'], row['color'],
                    row['weight'], row['price'], row['brand']
                ))
    except FileNotFoundError:
        print(f"CSV file not found at {CSV_FILE}")
    except Exception as e:
        print(f"Error loading products: {e}")

def save_product(values):
    """Save a new product to the CSV file"""
    try:
        # Check if file exists
        file_exists = os.path.isfile(CSV_FILE)
        
        # Open file in append mode
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            
            # Write headers if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write the new product
            writer.writerow(dict(zip(columns, values)))
            
        return True
    except Exception as e:
        print(f"Error saving product: {e}")
        return False

def show_add_dialog():
    print("Opening add dialog...")
    # Check if dialog already exists
    if hasattr(show_add_dialog, 'dialog_open') and show_add_dialog.dialog_open:
        return
    show_add_dialog.dialog_open = True
    
    dialog = tk.Toplevel(root)
    dialog.transient(root)
    dialog.grab_set()
    dialog.title("Add New Product")
    dialog.geometry("500x500")
    dialog.configure(bg=DARK_BG)
        
    def on_dialog_close():
        show_add_dialog.dialog_open = False
        dialog.destroy()
    
    dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
    
    entries = {}
    fields = columns
    current_color = tk.StringVar(value="#000000")

    def pick_color():
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:  # If a color was picked (not cancelled)
            current_color.set(color)
            color_preview.configure(background=color)
            entries['color'].configure(state='normal')
            entries['color'].delete(0, tk.END)
            entries['color'].insert(0, color)
            entries['color'].configure(state='readonly')

    for idx, field in enumerate(fields):
        label = ttk.Label(dialog, text=field.capitalize()+":", style="TLabel")
        label.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
        
        if field == 'type':
            # Create combobox for type selection
            entry = ttk.Combobox(dialog, values=PRODUCT_TYPES, state='readonly', style='TCombobox')
            entry.set("Select Type")  # Default text
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
        elif field == 'color':
            # Create color picker section
            color_frame = ttk.Frame(dialog)
            color_frame.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
            
            entry = ttk.Entry(color_frame, textvariable=current_color, state='readonly')
            entry.pack(side=tk.LEFT, padx=(0, 5))
            
            color_preview = tk.Label(color_frame, width=3, background=current_color.get(), fg=DARK_FG)
            color_preview.pack(side=tk.LEFT, padx=(0, 5))
            
            color_button = ttk.Button(color_frame, text="Pick Color", command=pick_color)
            color_button.pack(side=tk.LEFT)
        else:
            entry = ttk.Entry(dialog, style="TEntry")
            entry.grid(row=idx, column=1, padx=10, pady=5)
        
        entries[field] = entry

    def submit():
        values = []
        for field in fields:
            if field == 'type':
                value = entries[field].get()
                if value == "Select Type":
                    messagebox.showerror("Error", "Please select a product type!")
                    return
                values.append(value)
            else:
                values.append(entries[field].get())
        
        if any(v.strip() == '' for v in values):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        # Save to CSV and update table
        if save_product(values):
            tree.insert('', tk.END, values=values)
            on_dialog_close()
        else:
            messagebox.showerror("Error", "Failed to save product!")

    submit_btn = ttk.Button(dialog, text="Add", command=submit, style="Custom.TButton")
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)

def delete_selected_product():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a product to delete.")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected product?")
    if not confirm:
        return
    # Get all products
    all_products = []
    for item in tree.get_children():
        all_products.append(tree.item(item)['values'])
    # Remove selected
    for item in selected:
        tree.delete(item)
    # Save remaining products to CSV
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for values in tree.get_children():
            writer.writerow(tree.item(values)['values'])

def edit_selected_product():
    print("the edit button was clicked")
    selected = tree.selection()

    print("the selected are", selected)
    if not selected:
        messagebox.showwarning("No selection", "Please select a product to edit.")
        return
    item = selected[0]
    old_values = tree.item(item)['values']
    
    print("the old values are", old_values)
    dialog = tk.Toplevel(root)
    dialog.transient(root)
    dialog.grab_set()
    dialog.title("Edit Product")
    dialog.geometry("500x500")
    dialog.configure(bg=DARK_BG)
    
    entries = {}
    fields = columns
    current_color = tk.StringVar(value=old_values[2])

    def pick_color():
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            current_color.set(color)
            color_preview.configure(background=color)
            entries['color'].configure(state='normal')
            entries['color'].delete(0, tk.END)
            entries['color'].insert(0, color)
            entries['color'].configure(state='readonly')

    for idx, field in enumerate(fields):
        label = ttk.Label(dialog, text=field.capitalize()+":", style="TLabel")
        label.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
        value = old_values[idx]
        if field == 'type':
            entry = ttk.Combobox(dialog, values=PRODUCT_TYPES, state='readonly', style='TCombobox')
            entry.set(value)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
        elif field == 'color':
            color_frame = ttk.Frame(dialog)
            color_frame.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(color_frame, textvariable=current_color, state='readonly')
            entry.pack(side=tk.LEFT, padx=(0, 5))
            color_preview = tk.Label(color_frame, width=3, background=current_color.get(), fg=DARK_FG)
            color_preview.pack(side=tk.LEFT, padx=(0, 5))
            color_button = ttk.Button(color_frame, text="Pick Color", command=pick_color)
            color_button.pack(side=tk.LEFT)
        else:
            entry = ttk.Entry(dialog, style="TEntry")
            entry.insert(0, value)
            entry.grid(row=idx, column=1, padx=10, pady=5)
        entries[field] = entry

    def submit():
        values = []
        for field in fields:
            if field == 'type':
                value = entries[field].get()
                if value == "Select Type":
                    messagebox.showerror("Error", "Please select a product type!")
                    return
                values.append(value)
            else:
                values.append(entries[field].get())
        if any(v.strip() == '' for v in values):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        # Update the tree
        tree.item(item, values=values)
        # Save all products to CSV
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for row_id in tree.get_children():
                writer.writerow(tree.item(row_id)['values'])
        dialog.destroy()

    submit_btn = ttk.Button(dialog, text="Save", command=submit, style="Custom.TButton")
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)

# Add basic buttons
add_button = tb.Button(top_frame, text="Add New", bootstyle="success-outline", width=12, command=show_add_dialog)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tb.Button(top_frame, text="Delete", bootstyle="danger-outline", width=12, command=delete_selected_product)
delete_button.pack(side=tk.LEFT, padx=5)

edit_button = tb.Button(top_frame, text="Edit", bootstyle="info-outline", width=12, command=edit_selected_product)
edit_button.pack(side=tk.LEFT, padx=5)

# --- Search Bar ---
search_var = tk.StringVar()

# (Optional) Add a search icon before the entry
search_icon = ttk.Label(top_frame, text="🔍", background=DARK_BG, foreground=DARK_ACCENT, font=("Arial", 14))
search_icon.pack(side=tk.LEFT, padx=(0, 2))

# Use the custom style for the search entry
search_entry = ttk.Entry(top_frame, textvariable=search_var, width=30, style="Search.TEntry")
search_entry.pack(side=tk.LEFT, padx=8, pady=4, ipady=2)

def search_products():
    query = search_var.get().lower().strip()
    if not query:
        load_products()
        return
    # Clear table
    for item in tree.get_children():
        tree.delete(item)
    # Search in CSV
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if any(query in str(row[col]).lower() for col in columns):
                tree.insert('', tk.END, values=(
                    row['name'], row['type'], row['color'],
                    row['weight'], row['price'], row['brand']
                ))

def reset_search():
    search_var.set("")
    load_products()

search_button = tb.Button(top_frame, text="Search", bootstyle="primary-outline", width=10, command=search_products)
search_button.pack(side=tk.LEFT, padx=2)

reset_button = tb.Button(top_frame, text="Reset", bootstyle="secondary-outline", width=10, command=reset_search)
reset_button.pack(side=tk.LEFT, padx=2)

# Load products when starting the application
load_products()

# Start the application
root.mainloop()