import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from PIL import ImageTk, Image
import threading
import time

import pandas as pd
import chardet

def process_csv_and_save():
    # This function is executed in a separate thread to prevent freezing the GUI
    progress_bar['value'] = 0  # Reset progress bar
    progress_bar['maximum'] = 100  # Set maximum value of progress bar
    for i in range(101):
        progress_bar['value'] = i  # Update progress bar value
        app.update_idletasks()  # Update GUI
        time.sleep(0.03)  # Adjust the sleep time for smoother progress
    try:
        # Process CSV file
        file = pd.read_csv(filename, encoding='latin1')
        file['date'] = pd.to_datetime(file['Date/Time'], dayfirst=True).dt.date
        file['time'] = pd.to_datetime(file['Date/Time'], dayfirst=True).dt.time
        file = file.groupby(['Name', 'date']).agg({'time': ['min', 'max']})
        file.columns = ['Time_in', 'Time_out']
        
        # Save processed data to a new CSV file
        output_filename = filedialog.asksaveasfilename(title="Save Processed CSV file", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_filename:
            file.to_csv(output_filename)
            messagebox.showinfo("Success", "Processed data saved to:\n{}".format(output_filename))
    except Exception as e:
        messagebox.showerror("Error", "Error processing CSV file:\n{}".format(e))
    finally:
        progress_bar['value'] = 0  # Reset progress bar

def process_csv():
    global filename
    filename = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if filename:
        # Detect file encoding
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
            print(result['encoding'])
        
        # Create and start a new thread to process CSV and save
        threading.Thread(target=process_csv_and_save).start()

# Create the main application window
app = tk.Tk()
app.title("ZINGSA Attendance Processing")  # Set the window title

# Check if the script is bundled by PyInstaller
if hasattr(sys, '_MEIPASS'):
    # If bundled, adjust the image path to the temporary directory created by PyInstaller
    image_path = os.path.join(sys._MEIPASS, 'logo.png')
else:
    # If running as a script, use the normal image path
    image_path = 'logo.png'

# Load and display the logo image
logo_img = Image.open(image_path)
logo_img = logo_img.resize((200, 200), Image.LANCZOS)  # Resize the image
logo_img = ImageTk.PhotoImage(logo_img)  # Convert the image to Tkinter-compatible format
logo_label = tk.Label(app, image=logo_img)
logo_label.pack()

# Create a heading label
heading_label = tk.Label(app, text="ZINGSA Attendance Processing", font=("Helvetica", 16, "bold"))
heading_label.pack()

# Create a button to trigger CSV processing
process_button = tk.Button(app, text="Process CSV", command=process_csv)
process_button.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(app, orient='horizontal', mode='determinate')
progress_bar.pack(fill='x')

# Run the application loop
app.mainloop()
