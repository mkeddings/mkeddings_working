import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

folder_selected = filedialog.askdirectory(title="Select a Folder")

print(f"Selected Folder: {folder_selected}")

