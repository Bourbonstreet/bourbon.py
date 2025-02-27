import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
def get_fox_image_url():
    response = requests.get("https://randomfox.ca/floof/")
    if response.status_code == 200:
        return response.json()["image"]
    else:
        return None

def update_image(label):
    image_url = get_fox_image_url()
    if image_url:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_data = BytesIO(image_response.content)
            image = Image.open(image_data)
            image = image.resize((400, 400))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
root = tk.Tk()
root.title("Random Fox Picture Generator")
root.geometry("500x500")

image_label = tk.Label(root)
image_label.pack(pady=20)

fetch_button = ttk.Button(root, text="Next Picture", command=lambda: update_image(image_label))
fetch_button.pack(pady=10)

update_image(image_label)

root.mainloop()
