import json
import os
import tkinter as tk
from tkinter import messagebox
import requests


def toggle_input_fields():
    use_json = use_json_var.get()
    if use_json:
        username_label.pack_forget()
        username_entry.pack_forget()
        avatar_url_label.pack_forget()
        avatar_url_entry.pack_forget()
        content_label.pack_forget()
        content_entry.pack_forget()
        json_label.pack()
        json_entry.pack()
        json_entry.config(state=tk.NORMAL)
    else:
        json_label.pack_forget()
        json_entry.pack_forget()
        username_label.pack()
        username_entry.pack()
        avatar_url_label.pack()
        avatar_url_entry.pack()
        content_label.pack()
        content_entry.pack()
        json_entry.config(state=tk.DISABLED)


def send_webhook():
    webhook_url = webhook_url_entry.get().strip()
    if not webhook_url:
        messagebox.showerror("Error", "Please enter a valid Webhook URL.")
        return
    
    confirmation_message = None

    if use_json_var.get():
        json_data = json_entry.get("1.0", "end-1c").strip()

        if not json_data:
            messagebox.showerror("Error", "Please enter valid JSON data.")
            return

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON data: {str(e)}")
            return

        confirmation_message = (
            "Is this correct?\n Webhook URL:\n{}\nJSON data:\n{}\n".format(webhook_url, json.dumps(data, indent=4))
        )
    else:
        username = username_entry.get().strip()
        avatar_url = avatar_url_entry.get().strip()
        content = content_entry.get().strip()
        
        if not (username and content):
            messagebox.showerror("Error", "Username and Content cannot be empty.")
            return
        
        default_avatar_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png"

        if not avatar_url:
            avatar_url = default_avatar_url

        invalid_avatar = 0 if avatar_url.endswith((".jpg", ".jpeg", ".png", ".gif")) else 1

        if invalid_avatar == 1:
            messagebox.showerror("Error", "Invalid URL for Avatar.")
            return

        confirmation_message = (
            f"Is this correct?\n Username: {username}\n Profile image URL: "
            f"{avatar_url if avatar_url != default_avatar_url else 'default'}\n Content: {content}\n"
        )

        data = {
            "username": username,
            "avatar_url": avatar_url,
            "content": content,
        }
 
    confirmation = messagebox.askyesno("Confirmation", confirmation_message)

    if not confirmation:
        messagebox.showinfo("Cancelled", "Operation cancelled.")
        return

    try:
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 204:
            messagebox.showinfo("Success", "Webhook sent successfully!")
        else:
            messagebox.showerror("Error", f"Failed to send the webhook.\n{response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred while sending the webhook:\n{str(e)}")


# Create the main tkinter window
root = tk.Tk()
root.title("Webhook Sender")

# Get the path to the custom icon in the Assets subdirectory
icon_path = os.path.join(os.path.dirname(__file__), "Assets", "app.ico")

# Load the custom icon and set it for the tkinter window
root.iconbitmap(icon_path)

# Create and position webhook input box
webhook_url_label = tk.Label(root, text="Enter the Webhook URL here")
webhook_url_label.pack()
webhook_url_entry = tk.Entry(root)
webhook_url_entry.pack()

# Create and position the JSON data entry field
json_label = tk.Label(root, text="Enter custom JSON data:")
json_label.pack()
json_entry = tk.Text(root, width=50, height=10, state=tk.DISABLED)
json_entry.pack_forget()

# Create a checkbox to switch between basic input boxes and custom JSON
use_json_var = tk.BooleanVar()
use_json_var.set(False)  # Default is basic input boxes
use_json_checkbox = tk.Checkbutton(
    root, text="Use Custom JSON", variable=use_json_var, command=toggle_input_fields
)
use_json_checkbox.pack()

# Create and position the basic input fields
username_label = tk.Label(root, text="What should the Webhook name be?")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

avatar_url_label = tk.Label(
    root, text="Paste link to pfp image (or leave blank for default):"
)
avatar_url_label.pack()
avatar_url_entry = tk.Entry(root)
avatar_url_entry.pack()

content_label = tk.Label(root, text="What should message content be?")
content_label.pack()
content_entry = tk.Entry(root)
content_entry.pack()

# Create and position the "Send Webhook" button
send_button = tk.Button(root, text="Send Webhook", command=send_webhook)
send_button.pack()

# Start the main event loop
root.mainloop()

exit()