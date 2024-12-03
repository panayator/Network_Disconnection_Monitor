import time
import datetime
import os
import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

# Initialize disconnection counter, log file path, and disconnection tracking variables
disconnection_count = 0
log_file = "network_disconnect_log.txt"
disconnection_start_time = None
last_log_index = None  # Track the index of the last log entry in the text widget
min_disconnection_duration = 60  # Minimum duration in seconds to log a disconnection

# Function to check if the network is connected
def is_connected():
    try:
        # Attempt to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Function to log a disconnection entry
def log_disconnection():
    global disconnection_count, disconnection_start_time, last_log_index
    disconnection_count += 1
    counter_label.config(text=f"Disconnection Count: {disconnection_count}")
    disconnection_start_time = datetime.datetime.now()
    log_message = f"Disconnection {disconnection_count}: {disconnection_start_time.strftime('%Y-%m-%d from %H:%M:%S')} to "
    
    # Insert the complete disconnection message into the GUI and track its starting index
    last_log_index = log_display.index(tk.END)
    log_display.insert(tk.END, log_message)
    log_display.see(tk.END)
    print(f"Disconnection detected at index {last_log_index}")


# Function to complete a disconnection entry and update the window
def complete_disconnection_log():
    global disconnection_start_time, last_log_index
    reconnection_time = datetime.datetime.now()
    duration = reconnection_time - disconnection_start_time
    duration_seconds = duration.total_seconds()

    duration_str = str(duration).split(".")[0]  # Remove microseconds
    complete_message = f"{reconnection_time.strftime('%H:%M:%S')} (Duration: {duration_str})"
    
    # Complete the disconnection message in the GUI
    log_display.insert(last_log_index + "+1c", complete_message)
    log_display.see(tk.END)

    if duration_seconds >= min_disconnection_duration:
        # Add extra newline for longer disconnections and log to file
        log_display.insert(tk.END, "\n\n")
        log_display.see(tk.END)
        print(f"Logged at index Disconnection {last_log_index} {disconnection_count}: {disconnection_start_time.strftime('%Y-%m-%d from %H:%M:%S')} to {reconnection_time.strftime('%H:%M:%S')} (Duration: {duration_str})")
        with open(log_file, "a") as file:
            file.write(f"Disconnection {disconnection_count}: {disconnection_start_time.strftime('%Y-%m-%d from %H:%M:%S')} to {reconnection_time.strftime('%H:%M:%S')} (Duration: {duration_str})\n\n")
    else:
        # Show short disconnection message and schedule deletion
        info_label.config(text="Disconnection too short, deleting...")
        print(f"Disconnection too short, deleting...")

        def delete_log_entry():
            global disconnection_count
            try:
                # Delete from the start of the last line to just before the end
                log_display.delete("end-1l", "end-1c")
                log_display.see(tk.END)
                
                disconnection_count -= 1  # Adjust the count only if deleted
                info_label.config(text="")  # Clear info label after deletion
                counter_label.config(text=f"Disconnection Count: {disconnection_count}")
            except Exception as e:
                print(f"Error deleting the last entry: {e}")

        # Schedule the deletion with a 2-second delay
        window.after(2000, delete_log_entry)

        print(f"Short disconnection deleted.")

    # Update disconnection start time but do not reset last_log_index here
    disconnection_start_time = None


# Function to load previous disconnections from the log file
def load_previous_disconnections():
    global disconnection_count
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            log_entries = file.readlines()
            disconnection_count = int(len(log_entries) / 2)  # Set disconnection count to the number of previous entries
            for entry in log_entries:
                log_display.insert(tk.END, entry)
        counter_label.config(text=f"Disconnection Count: {disconnection_count}")
        log_display.see(tk.END)  # Scroll to the latest entry

# Function to refresh the log display on pressing F5
def refresh_log_display(event=None):
    global disconnection_count
    log_display.delete("1.0", tk.END)  # Clear the text area
    disconnection_count = 0  # Reset count before reloading
    load_previous_disconnections()  # Reload entries from the log file

# Function to continuously monitor the network and track disconnections
def monitor_network():
    global disconnection_start_time
    while True:
        if not is_connected():
            if disconnection_start_time is None:
                # Begin logging the disconnection
                log_disconnection()
        else:
            if disconnection_start_time:
                # Complete the log if there was an active disconnection
                complete_disconnection_log()
        time.sleep(10)  # Wait 10 seconds before checking again

# Setting up the Tkinter GUI
window = tk.Tk()
window.title("Network Disconnection Monitor")
window.geometry("600x500")

# Disconnection counter label
counter_label = tk.Label(window, text="Disconnection Count: 0", font=("Arial", 14))
counter_label.pack(pady=10)

# Information label for short disconnections
info_label = tk.Label(window, text="", font=("Arial", 10), fg="red")
info_label.pack()

# Scrollable text area to log disconnections
log_display = scrolledtext.ScrolledText(window, width=70, height=20, font=("Arial", 10))
log_display.pack(pady=10)

# Load previous disconnections when the program starts
load_previous_disconnections()

# Bind F5 key to refresh the log display
window.bind("<F5>", refresh_log_display)

# Run the network monitoring in a separate thread to keep the GUI responsive
monitor_thread = threading.Thread(target=monitor_network, daemon=True)
monitor_thread.start()

# Start the Tkinter main loop
window.mainloop()
