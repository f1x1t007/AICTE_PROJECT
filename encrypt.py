import cv2
import os

# Get the image path from the user
image_path = input("Enter the image path: ")
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not open image. Please check the path.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Store message length in the first pixel
msg_length = len(msg)
img[0, 0, 0] = msg_length  

d = {chr(i): i for i in range(255)}

n, m, z = 0, 0, 1  # Start from (0,0,1) since (0,0,0) is used for length

for char in msg:
    img[n, m, z] = d[char]
    z = (z + 1) % 3
    if z == 0:
        m += 1
    if m >= img.shape[1]:  # Move to the next row if needed
        m = 0
        n += 1

# Save encrypted image in the same folder
image_dir = os.path.dirname(image_path)
encrypted_image_path = os.path.join(image_dir, "encryptedImage.png")
cv2.imwrite(encrypted_image_path, img)

# Save the passcode in the same folder
passcode_path = os.path.join(image_dir, "passcode.txt")
with open(passcode_path, "w") as f:
    f.write(password)

print(f"Encryption complete! Encrypted image saved as: {encrypted_image_path}")
print(f"Passcode saved in: {passcode_path}")
