import os
import numpy as np
from PIL import Image, ImageOps, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog
from tensorflow.keras.models import load_model
from tkinter import ttk
from datetime import datetime

# -----------------------------
# Load model and labels
# -----------------------------
model = load_model("keras_Model.h5", compile=False)
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# -----------------------------
# History storage
# -----------------------------
history = []

def add_to_history(image_path, class_name, confidence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append((timestamp, image_path, class_name, confidence))

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Prediction History")
    history_window.configure(bg="black")
    history_window.geometry("700x500")

    tk.Label(history_window, text="Prediction History", font=("Arial", 24, "bold"),
             bg="black", fg="#FFD700").pack(pady=20)

    frame = tk.Frame(history_window, bg="black")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="black")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="black")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add history entries
    for entry in reversed(history):  # latest first
        timestamp, path, class_name, confidence = entry
        color = "#FF3333" if class_name.lower() == "rusted iron" else "#00FF00"
        tk.Label(scrollable_frame,
                 text=f"{timestamp} | {class_name} | {confidence:.2f}% | {os.path.basename(path)}",
                 font=("Arial", 14), bg="black", fg=color, anchor="w").pack(fill="x", padx=10, pady=2)

# -----------------------------
# Prediction function
# -----------------------------
glow_active = False
glow_phase = 0

def predict_image(image_path):
    global glow_active
    if not os.path.exists(image_path):
        result_label.config(text=f"File not found:\n{image_path}", fg="red")
        progress['value'] = 0
        return

    img = Image.open(image_path).convert("RGB")
    img_resized = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
    img_array = np.asarray(img_resized)
    normalized_array = (img_array.astype(np.float32) / 127.5) - 1
    data = np.expand_dims(normalized_array, axis=0)

    prediction = model.predict(data)
    index = np.argmax(prediction[0])
    class_name = class_names[index]
    confidence = prediction[0][index] * 100

    # Store in history
    add_to_history(image_path, class_name, confidence)

    # Dynamic color
    if class_name.lower() == "rusted iron":
        color = "#FF3333"  # red
        start_glow_animation()
    else:
        color = "#00FF00"
        stop_glow_animation()

    result_label.config(text=f"Class: {class_name}", fg=color)
    style.configure("Custom.Horizontal.TProgressbar", troughcolor='black', background=color)
    progress['value'] = confidence
    progress_label.config(text=f"{confidence:.2f}% Confidence", fg=color)

# -----------------------------


# Rounded image display
# -----------------------------
def round_image(img, size=(200, 200)):
    img = img.resize(size)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img_rounded = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    img_rounded.putalpha(mask)
    return ImageTk.PhotoImage(img_rounded)

# -----------------------------
# Glow animation
# -----------------------------
def glow_animation():
    global glow_phase
    if not glow_active:
        return
    glow_phase = (glow_phase + 0.05) % 1.0
    alpha = int((0.5 + 0.5 * np.sin(glow_phase * 2 * np.pi)) * 255)
    glow_size = 220
    glow_img = Image.new('RGBA', (glow_size, glow_size), (255,0,0,0))
    mask = Image.new('L', (glow_size, glow_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,glow_size,glow_size), fill=alpha)
    glow_img.putalpha(mask)
    glow_tk = ImageTk.PhotoImage(glow_img)
    glow_label.config(image=glow_tk)
    glow_label.image = glow_tk
    root.after(50, glow_animation)

def start_glow_animation():
    global glow_active
    glow_active = True
    glow_label.place(relx=0.5, rely=0.45, anchor='center')
    glow_animation()

def stop_glow_animation():
    global glow_active
    glow_active = False
    glow_label.place_forget()

# -----------------------------
# Shimmer title
# -----------------------------
shimmer_phase = 0
def shimmer_title():
    global shimmer_phase
    r = 255
    g = int((np.sin(shimmer_phase)+1)/2 * 255)
    b = 0
    color = f"#{r:02X}{g:02X}{b:02X}"
    title_label.config(fg=color)
    shimmer_phase += 0.05
    root.after(100, shimmer_title)

# -----------------------------
# Select image
# -----------------------------
def select_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        img = Image.open(file_path)
        img_tk = round_image(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        predict_image(file_path)

# -----------------------------
# Hover effect for button
# -----------------------------
def on_enter(e):
    select_button.config(bg="#555555")
def on_leave(e):
    select_button.config(bg="#333333")

# -----------------------------
# GUI setup
# -----------------------------
root = tk.Tk()
root.title("Iron Rust Detector")
root.attributes('-fullscreen', True)
root.resizable(False, False)
root.configure(bg="black")
root.bind("<Escape>", lambda e: root.destroy())

# Icon
try:
    root.iconbitmap(r"C:\Users\sssid\Downloads\Inail.ico")
except:
    print("Icon not found or invalid format.")

# Title
title_label = tk.Label(root, text="🛠 Iron Rust Detector 🛠", font=("Arial", 36, "bold"), bg="black", fg="#FFD700")
title_label.pack(pady=40)
shimmer_title()

# Glow behind image
glow_label = tk.Label(root, bg="black")
glow_label.place_forget()

# Buttons
select_button = tk.Button(root, text="Select Image", font=("Arial", 22, "bold"),
                          bg="#333333", fg="white", activebackground="#555555",
                          activeforeground="white", relief="flat", padx=40, pady=15,
                          command=select_image)
select_button.pack(pady=20)
select_button.bind("<Enter>", on_enter)
select_button.bind("<Leave>", on_leave)

history_button = tk.Button(root, text="View History", font=("Arial", 18, "bold"),
                           bg="#222222", fg="white", activebackground="#444444",
                           activeforeground="white", relief="flat", padx=30, pady=10,
                           command=view_history)
history_button.pack(pady=10)

# Image
image_label = tk.Label(root, bg="black")
image_label.pack(pady=20)

# Result
result_label = tk.Label(root, text="", font=("Arial", 28, "bold"), bg="black", fg="#00FF00")
result_label.pack(pady=20)

# Progress
style = ttk.Style()
style.theme_use('default')
style.configure("Custom.Horizontal.TProgressbar", troughcolor='black', background="#00FF00", thickness=25)
progress = ttk.Progressbar(root, style="Custom.Horizontal.TProgressbar", orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)
progress_label = tk.Label(root, text="", font=("Arial", 18), bg="black", fg="#00FF00")
progress_label.pack(pady=5)

# Close
close_button = tk.Button(root, text="Exit", font=("Arial", 18, "bold"),
                         bg="#222222", fg="white", activebackground="#444444",
                         activeforeground="white", relief="flat", padx=25, pady=10, command=root.destroy)
close_button.pack(side="bottom", pady=30)

# Run GUI
root.mainloop()
