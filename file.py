import tkinter as tk
from tkinter import filedialog
import zipfile
import os

# Function to create a zip archive of a folder
def create_zip_archive(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

# Event handler for the Browse button
def browse_button_clicked():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(tk.END, folder_path)

# Event handler for the Zip button
def zip_button_clicked():
    folder_path = folder_path_entry.get()
    if folder_path:
        zip_file_path = os.path.join(os.path.dirname(folder_path), 'archive.zip')
        create_zip_archive(folder_path, zip_file_path)
        tk.messagebox.showinfo('Success', 'Folder archived and compressed successfully.')
    else:
        tk.messagebox.showerror('Error', 'Please enter or select a folder path.')

# Event handler for the Clear button
def clear_button_clicked():
    folder_path_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title('Vighneshs File Zipper')

# Function to set the custom window icon
def set_window_icon():
    icon_path = 'path_to_icon_file.ico'  # Replace with the path to your own icon file
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

# Set the window icon
set_window_icon()

# Caption Bar widgets
# Add the minimize and maximize buttons if needed (depends on the platform)
# root.attributes('-zoomed', True)  # Uncomment this line to maximize the window by default

# Client area widgets
folder_path_label = tk.Label(root, text='Folder Path:')
folder_path_label.pack()

folder_path_entry = tk.Entry(root)
folder_path_entry.pack()

browse_button = tk.Button(root, text='Browse', command=browse_button_clicked)
browse_button.pack()

zip_button = tk.Button(root, text='Zip', command=zip_button_clicked)
zip_button.pack()

clear_button = tk.Button(root, text='Clear', command=clear_button_clicked)
clear_button.pack()

root.mainloop()
