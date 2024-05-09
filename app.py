import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

import pandas as pd
import chardet

def process_csv():
    filename = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if filename:
        # Detect file encoding
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
            print(result['encoding'])
        
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
                print("Processed data saved to:", output_filename)
            else:
                print("No file selected for saving.")
        except Exception as e:
            print("Error processing CSV file:", e)

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

# Run the application loop
app.mainloop()
