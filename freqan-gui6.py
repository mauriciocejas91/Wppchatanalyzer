import pandas as pd
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import matplotlib.pyplot as plt
import zipfile
import os

# WhatsApp-like theme colors
whatsapp_green = "#25D366"
whatsapp_light_gray = "#ECE5DD"
whatsapp_dark_gray = "#075E54"
whatsapp_white = "#FFFFFF"

# Global variables to store chat data and selected analysis type
loaded_data = None
analysis_type = "weekly"  # Default type is weekly

# Function to load the chat file and store data
def load_chat_file(file_path):
    global loaded_data

    # If the file is a zip, extract the txt file
    if file_path.lower().endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
            if not txt_files:
                messagebox.showerror("Error", "No .txt file found in the .zip archive.")
                return
            # Extract the first .txt file found in the .zip
            with zip_ref.open(txt_files[0]) as file:
                chat_data = file.read().decode("utf-8").splitlines()
    else:
        # Load data directly from a .txt file
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_data = file.readlines()

    # Regular expression to match the WhatsApp date format "DD/MM/YYYY, hh:mm" or "D/M/YYYY, hh:mm"
    date_pattern = r"\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2}"

    # Initialize lists to store extracted data
    dates = []
    participants = []

    # Process each line of the chat
    for line in chat_data:
        if re.match(date_pattern, line):
            # Extract the date and the participant
            date_str, message = line.split(" - ", 1)
            if ": " in message:
                participant = message.split(": ", 1)[0]
                # Count messages, including multimedia messages like "<Multimedia omitido>"
                dates.append(date_str)
                participants.append(participant)

    # Convert the dates to datetime format
    dates = pd.to_datetime(dates, format='%d/%m/%Y, %H:%M')

    # Create a DataFrame with participants and their corresponding dates
    loaded_data = pd.DataFrame({'Date': dates, 'Participant': participants})

# Function to perform analysis (daily, weekly, or monthly) and display in the table
def perform_analysis(tree):
    global loaded_data, analysis_type
    if loaded_data is None:
        return  # No data loaded

    # Clear existing table data
    for row in tree.get_children():
        tree.delete(row)

    df = loaded_data.copy()

    # Dynamically identify unique participants in the chat
    unique_participants = df['Participant'].unique()

    # Set the date frequency for analysis type
    if analysis_type == "daily":
        df['Period'] = df['Date'].dt.to_period('D')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='D')
    elif analysis_type == "weekly":
        df['Period'] = df['Date'].dt.to_period('W')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='W-MON')
    elif analysis_type == "monthly":
        df['Period'] = df['Date'].dt.to_period('M')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='MS')

    # Group by period and participant to get message counts
    period_stats = df.groupby(['Period', 'Participant']).size().unstack(fill_value=0)

    # Reindex to ensure all periods are covered, filling missing periods with zeros
    period_stats = period_stats.reindex(all_periods.to_period(df['Period'].dt.freq), fill_value=0)

    # Update treeview columns dynamically based on unique participants
    tree["columns"] = ['Period'] + list(unique_participants)
    tree["show"] = "headings"
    
    # Define headings
    tree.heading('Period', text=analysis_type.capitalize())
    for participant in unique_participants:
        tree.heading(participant, text=participant)

    # Set column widths
    tree.column('Period', width=150)
    for participant in unique_participants:
        tree.column(participant, width=150)

    # Insert data into the Treeview table
    for index, row in period_stats.iterrows():
        values = [str(index)] + [int(row.get(participant, 0)) for participant in unique_participants]
        tree.insert('', 'end', values=values)

# Function to visualize the chart
def visualize_chart():
    global loaded_data, analysis_type
    if loaded_data is None:
        messagebox.showerror("Error", "No chat data loaded.")
        return

    df = loaded_data.copy()

    # Group the data based on the analysis type
    if analysis_type == "daily":
        df['Period'] = df['Date'].dt.to_period('D')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='D')
    elif analysis_type == "weekly":
        df['Period'] = df['Date'].dt.to_period('W')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='W-MON')
    elif analysis_type == "monthly":
        df['Period'] = df['Date'].dt.to_period('M')
        all_periods = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today(), freq='MS')

    # Group by period and participant to get message counts
    period_stats = df.groupby(['Period', 'Participant']).size().unstack(fill_value=0)

    # Reindex to ensure all periods are covered, filling missing periods with zeros
    period_stats = period_stats.reindex(all_periods.to_period(df['Period'].dt.freq), fill_value=0)

    # Plotting the chart
    period_stats.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set1')
    plt.title(f"Message Count by {analysis_type.capitalize()}")
    plt.xlabel(analysis_type.capitalize())
    plt.ylabel("Number of Messages")
    plt.xticks(rotation=45)
    plt.legend(title="Participants")
    plt.tight_layout()  # Adjust the layout
    plt.show()  # Show the plot

# Function to open the file dialog and load chat
def open_file_dialog(tree):
    file_path = filedialog.askopenfilename(
        title="Select WhatsApp Chat File",
        filetypes=[("Text Files and Zips", "*.txt *.zip")]
    )
    
    if file_path:
        load_chat_file(file_path)  # Load chat into memory
        perform_analysis(tree)  # Perform initial analysis (default is weekly)

# Function to handle drag-and-drop event
def on_drop(event, tree):
    file_path = event.data.strip('{}')  # Remove curly braces added by TkinterDnD
    load_chat_file(file_path)
    perform_analysis(tree)

# Set up the basic GUI window with TkinterDnD for drag-and-drop support
root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop
root.title("WhatsApp Chat Analyzer")
root.geometry("600x500")
root.config(bg=whatsapp_light_gray)

# Set up ttkbootstrap theme
style = ttk.Style()
style.theme_use("flatly")

# Create a label with WhatsApp-like styling
label = ttk.Label(root, text="WhatsApp Chat Analyzer", font=("Helvetica", 18, "bold"), bootstyle="primary")
label.pack(pady=20)

# Frame to hold the analysis type buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Function to set analysis type and update the table
def set_analysis_type(new_type, tree):
    global analysis_type
    analysis_type = new_type
    perform_analysis(tree)  # Update table with the new analysis type

# Create buttons to select analysis type (Daily, Weekly, Monthly)
ttk.Button(button_frame, text="Daily", command=lambda: set_analysis_type("daily", tree), bootstyle="success-outline", width=10).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Weekly", command=lambda: set_analysis_type("weekly", tree), bootstyle="success-outline", width=10).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Monthly", command=lambda: set_analysis_type("monthly", tree), bootstyle="success-outline", width=10).grid(row=0, column=2, padx=10)

# Create a modern button to open the file dialog
select_file_button = ttk.Button(root, text="Select WhatsApp Chat File", command=lambda: open_file_dialog(tree), bootstyle="success", width=25)
select_file_button.pack(pady=10)

# Create a button to visualize the chart
visualize_button = ttk.Button(root, text="Visualize Chart", command=visualize_chart, bootstyle="success", width=25)
visualize_button.pack(pady=10)

# Create a Treeview widget to display the analysis stats
tree = ttk.Treeview(root)
tree.pack(pady=20, expand=True, fill='both')

# Bind drag-and-drop event
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', lambda e: on_drop(e, tree))

# Start the GUI event loop
root.mainloop()