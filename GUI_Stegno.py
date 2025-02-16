import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def encrypt():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Could not open image")
        return
    
    msg = msg_entry.get()
    password = pass_entry.get()
    if not msg or not password:
        messagebox.showwarning("Warning", "Message and password cannot be empty!")
        return
    
    msg_length = len(msg)
    img[0, 0, 0] = msg_length
    
    d = {chr(i): i for i in range(255)}
    n, m, z = 0, 0, 1
    
    for char in msg:
        img[n, m, z] = d[char]
        z = (z + 1) % 3
        if z == 0:
            m += 1
        if m >= img.shape[1]:
            m = 0
            n += 1
    
    save_dir = os.path.dirname(file_path)
    encrypted_path = os.path.join(save_dir, "encryptedImage.png")
    cv2.imwrite(encrypted_path, img)
    
    pass_path = os.path.join(save_dir, "passcode.txt")
    with open(pass_path, "w") as f:
        f.write(password)
    
    messagebox.showinfo("Success", f"Encrypted image saved at: {encrypted_path}")

def decrypt():
    file_path = filedialog.askopenfilename(title="Select encrypted image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Could not open image")
        return
    
    save_dir = os.path.dirname(file_path)
    pass_path = os.path.join(save_dir, "passcode.txt")
    
    try:
        with open(pass_path, "r") as f:
            stored_password = f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "Passcode file not found!")
        return
    
    entered_pass = pass_entry.get()
    if entered_pass != stored_password:
        messagebox.showerror("Error", "Incorrect passcode!")
        return
    
    c = {i: chr(i) for i in range(255)}
    msg_length = img[0, 0, 0]
    
    message = ""
    n, m, z = 0, 0, 1
    for _ in range(msg_length):
        message += c[img[n, m, z]]
        z = (z + 1) % 3
        if z == 0:
            m += 1
        if m >= img.shape[1]:
            m = 0
            n += 1
    
    messagebox.showinfo("Decryption Successful", f"Decrypted Message: {message}")

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x350")
root.configure(bg="#2c3e50")

frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame.pack(pady=20)

tk.Label(frame, text="Secret Message:", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack()
msg_entry = ttk.Entry(frame, width=50)
msg_entry.pack(pady=5)

tk.Label(frame, text="Passcode:", fg="white", bg="#34495e", font=("Arial", 12, "bold")).pack()
pass_entry = ttk.Entry(frame, width=50, show="*")
pass_entry.pack(pady=5)

style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)

encrypt_button = ttk.Button(frame, text="Encrypt Image", command=encrypt)
encrypt_button.pack(pady=10)

decrypt_button = ttk.Button(frame, text="Decrypt Image", command=decrypt)
decrypt_button.pack(pady=10)

root.mainloop()