import requests
import tkinter as tk
from tkinter import messagebox


def send_webhook():
    webhook_url = webhook_url_entry.get().strip()
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

    confirmation = messagebox.askyesno("Confirmation", confirmation_message)

    if confirmation:
        messagebox.showinfo("Webhook", "Okay, pinging webhook...")
        # webhook ping code
        data = {
            "username": username,
            "avatar_url": avatar_url,
            "content": content,
        }
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

# Set icon for tkinter window
icon_path = "Assets/app.ico"
root.iconbitmap(icon_path)

# Create and position labels and entry fields
webhook_url_label = tk.Label(root, text="Enter the Webhook URL here")
webhook_url_label.pack()
webhook_url_entry = tk.Entry(root)
webhook_url_entry.pack()

username_label = tk.Label(root, text="What should the Webhook name be?")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

avatar_url_label = tk.Label(root, text="Paste link to pfp image (or leave blank for default):")
avatar_url_label.pack()
avatar_url_entry = tk.Entry(root)
avatar_url_entry.pack()

content_label = tk.Label(root, text="What should message content be?")
content_label.pack()
content_entry = tk.Entry(root)
content_entry.pack()

send_button = tk.Button(root, text="Send Webhook", command=send_webhook)
send_button.pack()

# Start the main event loop
root.mainloop()
