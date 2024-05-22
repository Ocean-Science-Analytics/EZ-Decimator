# Created by Jared Stephens 08/11/2023
# This script analyzes and resamples WAV files to a predefined sampling rate from a user selected folder

# Pip install Pillow
import os
import librosa
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import threading

# Function to browse and set the input folder
def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_var.set(folder_path)

# Function to browse and set the output folder
def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

# Function to process a file
def process_file(filename, desired_sr):
    file_path = os.path.join(input_folder_var.get(), filename)
    y, sr = librosa.load(file_path, sr=None)
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=desired_sr)

    output_filename = get_output_filename(filename, desired_sr)
    output_path = os.path.join(output_folder_var.get(), output_filename)

    sf.write(output_path, y_resampled, desired_sr)

# Function to update the progress bar and status label
def update_progress(filename):
    progress['value'] += 1
    label_status.config(text=f'Processing: {filename}')
    root.update_idletasks()

# Function to process files and update progress bar
def process_files():
    input_folder = input_folder_var.get()
    desired_sr = int(desired_sr_entry.get())
    total_files = sum(1 for filename in os.listdir(input_folder) if filename.endswith(".wav"))
    progress['maximum'] = total_files

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            process_file(filename, desired_sr)
            update_progress(filename)

    messagebox.showinfo("Info", "Resampling and saving completed!")
    label_status.config(text='Resampling and saving completed.')
    progress['value'] = 0  # Reset the progress bar

# Function to performing process threading
def resample_and_save():
    # Create a thread to process the files
    processing_thread = threading.Thread(target=process_files)
    processing_thread.start()

# Function to get the modified output filename based on the checkbox state
def get_output_filename(filename, desired_sr):
    if include_sr_in_filename_var.get() == 1:
        return filename.replace(".wav", f"_{desired_sr}Hz.wav")
    else:
        return filename

# Create the main application window
root = tk.Tk()
root.title("WAV Decimator")
root.configure(bg='DodgerBlue4')
root.geometry("800x600")

# Load the company logo image
logo_image = Image.open("white_square_OSA_med.jpg")
logo_image = logo_image.resize((100, 100), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Display the company logo at the top left
logo_label = tk.Label(root, image=logo_photo, bg='navy')
logo_label.image = logo_photo
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

# Add a label for "EZ Decimator" at the top
ez_decimator_label = tk.Label(root, text="EZ Decimator", bg='DodgerBlue4', fg='white', font=("Times New Roman", 24, "bold"))
ez_decimator_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

# Input folder selection
input_folder_var = tk.StringVar()
input_folder_label = tk.Label(root, text="Select input folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 14,))
input_folder_label.place(relx=0.3, rely=0.28, anchor=tk.CENTER)
input_folder_entry = tk.Entry(root, textvariable=input_folder_var, width=40)
input_folder_entry.place(relx=0.3, rely=0.32, anchor=tk.CENTER)
browse_input_button = tk.Button(root, text="Browse", width=15, command=browse_input_folder, bd=0)
browse_input_button.place(relx=0.3, rely=0.36, anchor=tk.CENTER)

# Output folder selection
output_folder_var = tk.StringVar()
output_folder_label = tk.Label(root, text="Select output folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 14,))
output_folder_label.place(relx=0.3, rely=0.47, anchor=tk.CENTER)
output_folder_entry = tk.Entry(root, textvariable=output_folder_var, width=40)
output_folder_entry.place(relx=0.3, rely=0.51, anchor=tk.CENTER)
browse_output_button = tk.Button(root, text="Browse", width=15, command=browse_output_folder, bd=0)
browse_output_button.place(relx=0.3, rely=0.55, anchor=tk.CENTER)

# Desired sampling rate
desired_sr_label = tk.Label(root, text="Desired Sampling Rate (Hz):", bg='DodgerBlue4', fg='white', font=("Times New Roman", 14,))
desired_sr_label.place(relx=0.7, rely=0.28, anchor=tk.CENTER)
desired_sr_entry = tk.Entry(root, width=30)
desired_sr_entry.place(relx=0.7, rely=0.32, anchor=tk.CENTER)

# Checkbox variable
include_sr_in_filename_var = tk.IntVar()

# Checkbox for including desired sampling rate in the filename
include_sr_checkbox = tk.Checkbutton(
    root, text="Include Desired SR in Filename", variable=include_sr_in_filename_var,
    bg='DodgerBlue4', fg='white', font=("Times New Roman", 14),
    selectcolor='DodgerBlue4'
)
include_sr_checkbox.place(relx=0.73, rely=0.51, anchor=tk.CENTER)

# Resample button
style = ttk.Style()
style.configure('TButton', font=('Times New Roman', 16))

resample_button = ttk.Button(root, text="Resample and Save", style='TButton', command=resample_and_save, width=18)
resample_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Create a progress bar
progress = Progressbar(root, length=300, mode='determinate')
progress.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# Add a label to show the current processing status
label_status = tk.Label(root, text='', bg='DodgerBlue4', fg='white', font=("Times New Roman", 12))
label_status.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

# Start the main event loop
root.mainloop()



