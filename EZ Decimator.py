# This script analyzes and resamples WAV files to a predefined sampling rate from a user selected folder
# Created by Jared Stephens 08/11/2023
# Edited: JS - 02/16/2024
    # Adjusted "process_files" and "get_output_filename" functions to accommodate .WAV and .aif files.
# Edits JS - 11/10/2024
    # Adjusted "process_files" and get_output_filename" fucntion to accomodate .flac files
    # Added a "compress_to_flac" function to convert .wav and .aif files to .flac
# Edited JS - 11/24/2024 
    # Updated the UI to include separate tabs for resampling and FLAC conversion
    # Fixed the bugs with the progress bar labels so it displays correct files being processed
# Edited JS - 01/27/2025 
    # Added a tab for converting .flac files to .wav files
    # Added help pages on each tab

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

##########################################################################
#       READ INPUT AND OUTPUT FOLDERS
##########################################################################

# Function to browse and set the input folder
def browse_input_folder(): # Resampling
    folder_path = filedialog.askdirectory()
    input_folder_var.set(folder_path)

def browse_input_folder2(): # Convert to FLAC
    folder_path = filedialog.askdirectory()
    input_folder_var2.set(folder_path)

def browse_input_folder3(): # Convert to WAV
    folder_path = filedialog.askdirectory()
    input_folder_var3.set(folder_path)

# Function to browse and set the output folder
def browse_output_folder(): # Resampling
    folder_path = filedialog.askdirectory()
    output_folder_var.set(folder_path)

def browse_output_folder2(): # Convert to FLAC
    folder_path = filedialog.askdirectory()
    output_folder_var2.set(folder_path)

def browse_output_folder3(): # Convert to WAV
    folder_path = filedialog.askdirectory()
    output_folder_var3.set(folder_path)

##########################################################################
#       FUNCTIONS TO RESAMPLE FILES AND UPDATE PROGRESS BAR
##########################################################################

# Function to resample a file
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

##########################################################################
#       FUNCTION TO READ FOLDER AND  APPLY RESAMPLING FUNCTION
##########################################################################

# Function to process files and update progress bar
def process_files():
    input_folder = input_folder_var.get()
    desired_sr = int(desired_sr_entry.get())
    files_to_process = [filename for filename in os.listdir(input_folder) if filename.lower().endswith((".wav", ".aif", ".flac", ".WAV"))]
    if not files_to_process:
        messagebox.showerror("Error", "No valid audio files found in the folder.")
        label_status.config(text='No valid audio files found.')
        return

    total_files = len(files_to_process)
    progress['maximum'] = total_files

    for idx, filename in enumerate(files_to_process, start=1):
        process_file(filename, desired_sr)

        # Update progress bar and status
        progress['value'] = idx
        label_status.config(text=f'Processing: {filename} ({idx}/{total_files})')
        root.update_idletasks()

    messagebox.showinfo("Info", "Resampling and saving completed!")
    label_status.config(text='Resampling and saving completed.')
    progress['value'] = 0  # Reset the progress bar


##########################################################################
#       FUNCTION TO CONVERT TO FLAC
##########################################################################

def compress_to_flac():
    input_folder = input_folder_var2.get()
    output_folder = output_folder_var2.get()
    files_to_compress = [f for f in os.listdir(input_folder) if f.lower().endswith((".wav", ".aif", ".WAV"))]
    
    if not files_to_compress:
        messagebox.showerror("Error", "Error: no .wav or .aif files found in the folder")
        label_status_tab2.config(text='No .wav or .aif files found.')
        return
    
    progress_tab2['maximum'] = len(files_to_compress)

    for idx, filename in enumerate(files_to_compress, start=1):
        file_path = os.path.join(input_folder, filename)
        y, sr = librosa.load(file_path, sr=None)

        # Construct the output file path
        output_filename = os.path.splitext(filename)[0] + ".flac"  # Change extension to .flac
        output_path = os.path.join(output_folder, output_filename)  # Combine folder and filename

        # Write to .flac file
        sf.write(output_path, y, sr, format='FLAC')

        # Update progress bar and status
        progress_tab2['value'] = idx
        label_status_tab2.config(text=f'Processing: {filename} ({idx}/{len(files_to_compress)})')
        root.update_idletasks()

    messagebox.showinfo("Info", "Compression to FLAC completed!")
    label_status_tab2.config(text='Compression to FLAC completed.')
    progress_tab2['value'] = 0  # Reset the progress bar


##########################################################################
#       FUNCTION TO CONVERT TO WAV
##########################################################################

def convert_to_wav():
    input_folder = input_folder_var3.get()
    output_folder = output_folder_var3.get()
    files_to_compress = [f for f in os.listdir(input_folder) if f.lower().endswith((".flac"))]
    
    if not files_to_compress:
        messagebox.showerror("Error", "Error: no .flac files found in the folder")
        label_status_tab3.config(text='No .flac files found.')
        return
    
    progress_tab3['maximum'] = len(files_to_compress)

    for idx, filename in enumerate(files_to_compress, start=1):
        file_path = os.path.join(input_folder, filename)
        y, sr = librosa.load(file_path, sr=None)

        # Construct the output file path
        output_filename = os.path.splitext(filename)[0] + ".wav"  # Change extension to .flac
        output_path = os.path.join(output_folder, output_filename)  # Combine folder and filename

        # Write to .flac file
        sf.write(output_path, y, sr, format='WAV')

        # Update progress bar and status
        progress_tab3['value'] = idx
        label_status_tab3.config(text=f'Processing: {filename} ({idx}/{len(files_to_compress)})')
        root.update_idletasks()

    messagebox.showinfo("Info", "Conversion to WAV completed!")
    label_status_tab3.config(text='Conversion to WAV completed.')
    progress_tab3['value'] = 0  # Reset the progress bar

##########################################################################
#       FUNCTIONS TO APPLY THREADING AND CHANGE FILE NAME (IF SELECTED)
##########################################################################

# Perform process threading
def resample_and_save():
    # Create a thread to process the files
    processing_thread = threading.Thread(target=process_files)
    processing_thread.start()

# Function to get the modified output filename based on the checkbox state
def get_output_filename(filename, desired_sr):
    if include_sr_in_filename_var.get() == 1:
        base, ext = os.path.splitext(filename)
        return f"{base}_{desired_sr}Hz{ext}"
    else:
        return filename

##########################################################################
#       HELP PAGES FOR EACH TAB
##########################################################################

# Help text function
def show_help():
    help_text = (
        "Welcome to EZ DECIMATOR!\n\n"
        "This tab allows you to resample audio files based on a given sampling rate. To use this program, simply:\n\n"
        "   1. Provide the input folder with original audio files.\n\n"
        "   2. Provide the output folder in which the files will be\n"
        "       downloaded too.\n\n"
        "   3. Insert the desired sampling rate.\n\n"
        "   4. Select if the sampling rate should be included in the file\n"
        "       name of the new resampled files. \n\n"
        "   5. Click 'Resample and Save'.\n\n"
        "Thank you for using EZ DECIMATOR!"
    )
    messagebox.showinfo("Help", help_text)

def show_help2():
    help_text = (
        "This tab allows you to convert .wav, .WAV, or .aif files to .flac format. To use this program, simply:\n\n"
        "   1. Provide the input folder with original audio files.\n\n"
        "   2. Provide the output folder in which the files will be\n"
        "       downloaded too.\n\n"
        "   3. Click 'Convert to FLAC'.\n\n"
        "Thank you for using EZ DECIMATOR!"
    )
    messagebox.showinfo("Help", help_text)

def show_help3():
    help_text = (
        "This tab allows you to convert .flac files to .wav format. To use this program, simply:\n\n"
        "   1. Provide the input folder with original audio files.\n\n"
        "   2. Provide the output folder in which the files will be\n"
        "       downloaded too.\n\n"
        "   3. Click 'Convert to WAV'\n\n"
        "Thank you for using EZ DECIMATOR!"
    )
    messagebox.showinfo("Help", help_text)



##########################################################################
#       GUI --> CREATE FRAME WITH TAB HEADERS
##########################################################################

# Create the main application window
root = tk.Tk()
root.title("EZ DECIMATOR")
root.configure(bg='DodgerBlue4')
root.geometry("800x600")

# Create a notebook for tabs at the very top
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for the two tabs
tab1 = tk.Frame(notebook, bg='DodgerBlue4')
tab2 = tk.Frame(notebook, bg='DodgerBlue4')
tab3 = tk.Frame(notebook, bg='DodgerBlue4')

notebook.add(tab1, text="Resampling")
notebook.add(tab2, text="FLAC Conversion")
notebook.add(tab3, text="WAV Conversion")

# Shared header: Logo and title in each tab
def create_tab_header(parent):
    # Create a frame for the header inside the parent tab
    header_frame = tk.Frame(parent, bg='DodgerBlue4')
    header_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10, fill=tk.X)

    # Load the company logo image
    logo_image = Image.open("white_square_OSA_med.jpg")
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Display the company logo
    logo_label = tk.Label(header_frame, image=logo_photo, bg='DodgerBlue4')
    logo_label.image = logo_photo  # Keep reference to avoid garbage collection
    logo_label.pack(side=tk.LEFT)

    # Add a label for "EZ Decimator" next to the logo
    ez_decimator_label = tk.Label(
        header_frame, text="EZ DECIMATOR", bg='DodgerBlue4', fg='white',
        font=("Times New Roman", 24, "bold")
    )
    ez_decimator_label.pack(side=tk.LEFT, padx=10)

# Add the shared header to each tab
create_tab_header(tab1)
create_tab_header(tab2)
create_tab_header(tab3)

##########################################################################
#       GUI --> TAB 1 = VARIABLES, HELP BUTTON, AND BOARDER
##########################################################################

# Tab 1: Resampling UI
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
include_sr_in_filename_var = tk.IntVar()

# Add help button function and placement on tab1
help_button_tab1 = tk.Button(tab1, text="HELP", bg='gray', fg='white', font=("Times New Roman", 16), command=show_help)
help_button_tab1.pack(padx=10, pady=10)
help_button_tab1.place(relx=0.95, rely=0.06, anchor=tk.NE)

# Add a canvas to draw the border around the widgets
canvas_border1= tk.Canvas(tab1, bg='DodgerBlue4', highlightthickness=0)
canvas_border1.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=695, height=395)
# Draw the initial border
canvas_border1.create_rectangle(10, 10, 685, 385, outline="white", width=2)


##########################################################################
#       GUI --> TAB 1 = WIDGETS AND INPUTS
##########################################################################

# Input folder selection
input_folder_label = tk.Label(tab1, text="Select Input Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
input_folder_label.pack(pady=5)
input_folder_label.place(relx=0.3, rely=0.28, anchor=tk.CENTER)
input_folder_entry = tk.Entry(tab1, textvariable=input_folder_var, width=40)
input_folder_entry.pack(pady=5)
input_folder_entry.place(relx=0.3, rely=0.32, anchor=tk.CENTER)
browse_input_button = tk.Button(tab1, text="Browse", command=browse_input_folder, font=("Times New Roman", 12), bd=0, width=18)
browse_input_button.pack(pady=5)
browse_input_button.place(relx=0.3, rely=0.37, anchor=tk.CENTER)

# Output folder selection
output_folder_label = tk.Label(tab1, text="Select Output Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
output_folder_label.pack(pady=5)
output_folder_label.place(relx=0.3, rely=0.47, anchor=tk.CENTER)
output_folder_entry = tk.Entry(tab1, textvariable=output_folder_var, width=40)
output_folder_entry.pack(pady=5)
output_folder_entry.place(relx=0.3, rely=0.51, anchor=tk.CENTER)
browse_output_button = tk.Button(tab1, text="Browse", command=browse_output_folder, font=("Times New Roman", 12), bd=0, width=18)
browse_output_button.pack(pady=5)
browse_output_button.place(relx=0.3, rely=0.56, anchor=tk.CENTER)

# Desired sampling rate
desired_sr_label = tk.Label(tab1, text="Desired Sampling Rate (Hz):", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
desired_sr_label.pack(pady=5)
desired_sr_label.place(relx=0.7, rely=0.28, anchor=tk.CENTER)
desired_sr_entry = tk.Entry(tab1, width=40)
desired_sr_entry.pack(pady=5)
desired_sr_entry.place(relx=0.7, rely=0.32, anchor=tk.CENTER)

# Checkbox for including desired sampling rate in the filename
include_sr_checkbox = tk.Checkbutton(tab1, text="Include Desired SR in Filename", variable=include_sr_in_filename_var, bg='DodgerBlue4', fg='white', font=("Times New Roman", 16), selectcolor='DodgerBlue4')
include_sr_checkbox.pack(pady=5)
include_sr_checkbox.place(relx=0.73, rely=0.51, anchor=tk.CENTER)

# Resample button
resample_button = tk.Button(tab1, text="Resample and Save", bg='light blue', fg='black', font=("Times New Roman", 16), command=resample_and_save, width=20)
resample_button.pack(pady=20)
resample_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Progress bar and status label
progress = Progressbar(tab1, length=300, mode='determinate')
progress.pack(pady=5)
progress.place(relx=0.5, rely=0.81, anchor=tk.CENTER)
label_status = tk.Label(tab1, text='', bg='DodgerBlue4', fg='white', font=("Times New Roman", 12))
label_status.pack(pady=5)
label_status.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

##########################################################################
#       GUI --> TAB 2 = CONVERT TO FLAC
##########################################################################

# Tab 2: Compress to FLAC
input_folder_var2 = tk.StringVar()
output_folder_var2 = tk.StringVar()

help_button_tab2 = tk.Button(tab2, text="HELP", bg='gray', fg='white', font=("Times New Roman", 16), command=show_help2)
help_button_tab2.pack(padx=10, pady=10)
help_button_tab2.place(relx=0.95, rely=0.06, anchor=tk.NE)

# Add a canvas to draw the border around the widgets
canvas_border2= tk.Canvas(tab2, bg='DodgerBlue4', highlightthickness=0)
canvas_border2.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=695, height=395)
# Draw the initial border
canvas_border2.create_rectangle(10, 10, 685, 385, outline="white", width=2)

# Input folder selection
input_folder_label = tk.Label(tab2, text="Select Input Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
input_folder_label.pack(pady=5)
input_folder_label.place(relx=0.3, rely=0.28, anchor=tk.CENTER)
input_folder_entry = tk.Entry(tab2, textvariable=input_folder_var2, width=50)
input_folder_entry.pack(pady=5)
input_folder_entry.place(relx=0.6, rely=0.34, anchor=tk.CENTER)
browse_input_button = tk.Button(tab2, text="Browse", command=browse_input_folder2, font=("Times New Roman", 12), bd=0, width=16)
browse_input_button.pack(pady=5)
browse_input_button.place(relx=0.3, rely=0.34, anchor=tk.CENTER)

# Output folder selection
output_folder_label = tk.Label(tab2, text="Select Output Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
output_folder_label.pack(pady=5)
output_folder_label.place(relx=0.3, rely=0.47, anchor=tk.CENTER)
output_folder_entry = tk.Entry(tab2, textvariable=output_folder_var2, width=50)
output_folder_entry.pack(pady=5)
output_folder_entry.place(relx=0.6, rely=0.53, anchor=tk.CENTER)
browse_output_button = tk.Button(tab2, text="Browse", command=browse_output_folder2, font=("Times New Roman", 12), bd=0, width=16)
browse_output_button.pack(pady=5)
browse_output_button.place(relx=0.3, rely=0.53, anchor=tk.CENTER)

# Compress to  FLAC button
compress_button = tk.Button(tab2, text="Convert to FLAC", bg='light blue', fg='black', font=("Times New Roman", 16), command=compress_to_flac, width=20)
compress_button.pack(pady=20)
compress_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Progress bar and status label for Tab 2
progress_tab2 = Progressbar(tab2, length=300, mode='determinate')
progress_tab2.pack(pady=5)
progress_tab2.place(relx=0.5, rely=0.81, anchor=tk.CENTER)

label_status_tab2 = tk.Label(tab2, text='', bg='DodgerBlue4', fg='white', font=("Times New Roman", 12))
label_status_tab2.pack(pady=5)
label_status_tab2.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

##########################################################################
#       GUI --> TAB 3 = CONVERT TO WAV
##########################################################################

# Tab 3: Convert to WAV
input_folder_var3= tk.StringVar()
output_folder_var3 = tk.StringVar()

help_button_tab3 = tk.Button(tab3, text="HELP", bg='gray', fg='white', font=("Times New Roman", 16), command=show_help3)
help_button_tab3.pack(padx=10, pady=10)
help_button_tab3.place(relx=0.95, rely=0.06, anchor=tk.NE)

# Add a canvas to draw the border around the widgets
canvas_border3= tk.Canvas(tab3, bg='DodgerBlue4', highlightthickness=0)
canvas_border3.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=695, height=395)
# Draw the initial border
canvas_border3.create_rectangle(10, 10, 685, 385, outline="white", width=2)

# Input folder selection
input_folder_label = tk.Label(tab3, text="Select Input Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
input_folder_label.pack(pady=5)
input_folder_label.place(relx=0.3, rely=0.28, anchor=tk.CENTER)
input_folder_entry = tk.Entry(tab3, textvariable=input_folder_var3, width=50)
input_folder_entry.pack(pady=5)
input_folder_entry.place(relx=0.6, rely=0.34, anchor=tk.CENTER)
browse_input_button = tk.Button(tab3, text="Browse", command=browse_input_folder3, font=("Times New Roman", 12), bd=0, width=16)
browse_input_button.pack(pady=5)
browse_input_button.place(relx=0.3, rely=0.34, anchor=tk.CENTER)

# Output folder selection
output_folder_label = tk.Label(tab3, text="Select Output Folder:", bg='DodgerBlue4', fg='white', font=("Times New Roman", 16))
output_folder_label.pack(pady=5)
output_folder_label.place(relx=0.3, rely=0.47, anchor=tk.CENTER)
output_folder_entry = tk.Entry(tab3, textvariable=output_folder_var3, width=50)
output_folder_entry.pack(pady=5)
output_folder_entry.place(relx=0.6, rely=0.53, anchor=tk.CENTER)
browse_output_button = tk.Button(tab3, text="Browse", command=browse_output_folder3, font=("Times New Roman", 12), bd=0, width=16)
browse_output_button.pack(pady=5)
browse_output_button.place(relx=0.3, rely=0.53, anchor=tk.CENTER)

# Convert to WAV button
compress_button = tk.Button(tab3, text="Convert to WAV", bg='light blue', fg='black', font=("Times New Roman", 16), command=convert_to_wav, width=20)
compress_button.pack(pady=20)
compress_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Progress bar and status label for Tab 3
progress_tab3 = Progressbar(tab3, length=300, mode='determinate')
progress_tab3.pack(pady=5)
progress_tab3.place(relx=0.5, rely=0.81, anchor=tk.CENTER)

label_status_tab3 = tk.Label(tab3, text='', bg='DodgerBlue4', fg='white', font=("Times New Roman", 12))
label_status_tab3.pack(pady=5)
label_status_tab3.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

# Start the main event loop
root.mainloop()


