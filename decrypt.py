import cv2
import os

# Get the encrypted image path from the user
image_path = input("Enter the encrypted image path: ")
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not open image. Please check the path.")
    exit()

# Get the directory of the encrypted image
image_dir = os.path.dirname(image_path)
passcode_path = os.path.join(image_dir, "passcode.txt")

# Retrieve stored password
try:
    with open(passcode_path, "r") as f:
        stored_password = f.read().strip()
except FileNotFoundError:
    print("Error: Passcode file not found in the same folder as the encrypted image!")
    exit()

pas = input("Enter passcode for Decryption: ")

if stored_password == pas:
    c = {i: chr(i) for i in range(255)}

    # Read message length from the first pixel
    msg_length = img[0, 0, 0]
    
    message = ""
    n, m, z = 0, 0, 1  # Start from (0,0,1) since (0,0,0) is used for length

    for _ in range(msg_length):
        message += c[img[n, m, z]]
        z = (z + 1) % 3
        if z == 0:
            m += 1
        if m >= img.shape[1]:  # Move to the next row if needed
            m = 0
            n += 1

    print("Decryption message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")
