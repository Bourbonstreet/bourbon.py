import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Tkinter Game with Background")
root.geometry("800x600")

bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

player = canvas.create_oval(375, 275, 425, 325, fill="blue")
player_speed = 10

def move_player(event):
    if event.keysym == "Up":
        canvas.move(player, 0, -player_speed)
    elif event.keysym == "Down":
        canvas.move(player, 0, player_speed)
    elif event.keysym == "Left":
        canvas.move(player, -player_speed, 0)
    elif event.keysym == "Right":
        canvas.move(player, player_speed, 0)

root.bind("<Up>", move_player)
root.bind("<Down>", move_player)
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

root.mainloop()
