# Import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Server details
HOST = '127.0.0.1'
PORT = 1234

# Colors and Fonts
DARK_GREY = '#2C3E50'
MEDIUM_GREY = '#34495E'
OCEAN_BLUE = '#1ABC9C'
LIGHT_BLUE = '#A3E4D7'
WHITE = '#ECF0F1'
FONT = ("Arial", 16)
BUTTON_FONT = ("Arial", 14, "bold")
SMALL_FONT = ("Arial", 12)

# Create a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Add message to message box
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)

# Connect to the server
def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Connection Error", f"Unable to connect to server {HOST}:{PORT}")
        return

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Invalid Username", "Username cannot be empty")
        return

    # Start a thread to listen for messages from the server
    threading.Thread(target=listen_for_messages_from_server, args=(client,), daemon=True).start()

# Send a message to the server
def send_message():
    message = message_textbox.get()
    if message.strip() != '':
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty Message", "Message cannot be empty")

# Listen for messages from the server
def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split("~", 1)
                add_message(f"[{username}] {content}")
            else:
                add_message("[SERVER] Empty message received")
        except Exception as e:
            print(f"Error: {e}")
            break

# Graceful exit on close
def on_closing():
    try:
        client.close()
    except:
        pass
    root.destroy()

# Initialize GUI
root = tk.Tk()
root.geometry("600x700")
root.title("Enterprise Messenger")
root.configure(bg=DARK_GREY)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Top Frame (Username Input)
top_frame = tk.Frame(root, bg=MEDIUM_GREY, height=80)
top_frame.pack(fill=tk.X)

username_label = tk.Label(top_frame, text="Enter Username:", font=FONT, bg=MEDIUM_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10, pady=20)

username_textbox = tk.Entry(top_frame, font=FONT, bg=WHITE, fg=DARK_GREY, width=20, relief=tk.FLAT)
username_textbox.pack(side=tk.LEFT, padx=10)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, width=10, relief=tk.FLAT, command=connect)
username_button.pack(side=tk.LEFT, padx=10)

# Middle Frame (Message Display)
middle_frame = tk.Frame(root, bg=MEDIUM_GREY, height=500)
middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=LIGHT_BLUE, fg=DARK_GREY, width=65, height=25, state=tk.DISABLED, wrap=tk.WORD, relief=tk.FLAT)
message_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Bottom Frame (Message Input)
bottom_frame = tk.Frame(root, bg=MEDIUM_GREY, height=80)
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=WHITE, fg=DARK_GREY, width=40, relief=tk.FLAT)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, width=10, relief=tk.FLAT, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

# Start the GUI
root.mainloop()
