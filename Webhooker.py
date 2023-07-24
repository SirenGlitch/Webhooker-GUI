import requests
import tkinter as tk
from tkinter import messagebox
import json


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

    if use_json_var.get():
        json_data = json_entry.get("1.0", "end-1c").strip()

        if not json_data:
            messagebox.showerror("Error", "Please enter valid JSON data.")
            return

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON data: {e}")
            return

        confirmation_message = (
            "Is this correct?\n JSON data:\n{}\n".format(json.dumps(data, indent=4))
        )

    else:
        username = username_entry.get().strip()
        avatar_url = avatar_url_entry.get().strip()
        content = content_entry.get().strip()
        default_avatar_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png"

        if not avatar_url:
            avatar_url = default_avatar_url

        while True:
            if avatar_url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                break
            else:
                messagebox.showwarning("Invalid URL", f"Invalid URL: {avatar_url}")
                avatar_url = avatar_url_entry.get().strip()

        confirmation_message = (
            f"Is this correct?\n username: {username}\n Profile image URL: "
            f"{'default' if avatar_url == default_avatar_url else avatar_url}\n message: {content}\n"
        )
        data = {
            "username": username,
            "avatar_url": avatar_url,
            "content": content,
        }

    confirmation = messagebox.askyesno("Confirmation", confirmation_message)

    if confirmation:
        messagebox.showinfo("Webhook", "Okay, pinging webhook...")
        # webhook ping code
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            messagebox.showinfo("Webhook", "Webhook sent successfully!")
        else:
            messagebox.showerror("Webhook", "Failed to send the webhook.")

    else:
        messagebox.showinfo("Webhook", "Okay, cancelling...")
        exit()


# Create the main tkinter window
root = tk.Tk()
root.title("Webhook Sender")

# Set a custom icon for the window (replace "path/to/your/icon.ico" with your icon path)
icon_path = "Assets/app.ico"
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
