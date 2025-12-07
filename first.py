# ---------------------------------------------------
# SMART DORM MAP v2.2 - Final Presentation Version
# ---------------------------------------------------
# Features:
#  • 8AM–11PM time-slot reservations
#  • Reserver name input + cancellation
#  • Persistent data (room_status.txt)
#  • Occupancy counters
#  • File / Help menu
#  • Blurred background image (via Pillow)
#  • Balanced 2x2 grid layout (A1,A2,B1,B2)
# ---------------------------------------------------

import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from datetime import datetime
from PIL import Image, ImageTk
import os

# ---------- Configuration ----------
STATUS_FILE = "room_status.txt"
BACKGROUND_IMAGE = "uca_dorm_blurred.jpg"

rooms = {
    "A1": ["MV Lounge 1","MV Lounge 2","Study Room 1","Study Room 2","TV Lounge 1","TV Lounge 2"],
    "A2": ["MV Lounge 1","MV Lounge 2","Study Room 1","Study Room 2","TV Lounge 1","TV Lounge 2"],
    "B1": ["MV Lounge 1","MV Lounge 2","Study Room 1","Study Room 2","TV Lounge 1","TV Lounge 2"],
    "B2": ["MV Lounge 1","MV Lounge 2","Study Room 1","Study Room 2","TV Lounge 1","TV Lounge 2"]
}
TIME_SLOTS = [f"{h}:00-{h+1}:00 {'AM' if h < 12 else 'PM'}" for h in range(8, 23)]

# ---------- File Handling ----------
def load_status():
    data = {}
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 5:
                    b, r, s, n, t = parts
                    data.setdefault((b, r), {})[s] = (n, t)
    return data

def save_status():
    with open(STATUS_FILE, "w") as f:
        for (b, r), reservations in room_states.items():
            for s, (n, t) in reservations.items():
                f.write(f"{b}:{r}:{s}:{n}:{t}\n")

# ---------- Logic ----------
def count_reserved(block):
    tot = len(rooms[block])
    res = sum(1 for r in rooms[block] if room_states.get((block, r)))
    return res, tot

def update_counter(block):
    occ, tot = count_reserved(block)
    counters[block].config(text=f"{occ} / {tot} Rooms Reserved")

def refresh_button(block, room):
    key = (block, room)
    res = room_states.get(key, {})
    btn = buttons[key]
    if not res:
        btn.config(bg="#27ae60", fg="white", text=f"{room}\nAvailable")
    elif len(res) < len(TIME_SLOTS):
        btn.config(bg="#f1c40f", fg="black", text=f"{room}\nReserved ({len(res)})")
    else:
        btn.config(bg="#e74c3c", fg="white", text=f"{room}\nFully Booked")
    update_counter(block)

# ---------- Reservation Popup ----------
def show_details(block, room):
    popup = Toplevel(root)
    popup.title(f"{block} - {room}")
    popup.geometry("430x420")
    popup.configure(bg="#fdfdfd")

    tk.Label(popup, text=f"{block} • {room}",
             font=("Segoe UI", 13, "bold"), bg="#fdfdfd").pack(pady=8)

    frame = tk.Frame(popup, bg="#fdfdfd")
    frame.pack(pady=5)

    tk.Label(frame, text="Current Reservations:",
             bg="#fdfdfd", font=("Segoe UI", 10, "underline")).pack(anchor="w")

    reservations = room_states.get((block, room), {})
    if reservations:
        for s, (n, t) in reservations.items():
            tk.Label(frame, text=f"• {s}  →  {n}  ({t})",
                     bg="#fdfdfd", anchor="w").pack(fill="x")
    else:
        tk.Label(frame, text="No reservations yet.", bg="#fdfdfd").pack(anchor="w")

    form = tk.Frame(popup, bg="#fdfdfd")
    form.pack(pady=15)

    tk.Label(form, text="Select Time Slot:", bg="#fdfdfd").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    slot_box = ttk.Combobox(form, values=TIME_SLOTS, width=25)
    slot_box.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Your Name:", bg="#fdfdfd").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form, width=28)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    def reserve():
        slot, name = slot_box.get(), name_entry.get().strip()
        if not slot or not name:
            messagebox.showwarning("Incomplete", "Enter name and select slot.")
            return
        res = room_states.setdefault((block, room), {})
        if slot in res:
            messagebox.showerror("Conflict", "This slot is already reserved.")
            return
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        res[slot] = (name, stamp)
        save_status()
        refresh_button(block, room)
        popup.destroy()
        messagebox.showinfo("Reserved", f"{room} reserved for {slot} by {name}.")

    def cancel():
        slot = slot_box.get()
        if not slot:
            messagebox.showwarning("Select Slot", "Select a slot to cancel.")
            return
        if slot in room_states.get((block, room), {}):
            del room_states[(block, room)][slot]
            if not room_states[(block, room)]:
                del room_states[(block, room)]
            save_status()
            refresh_button(block, room)
            popup.destroy()
            messagebox.showinfo("Cancelled", f"Reservation for {slot} cancelled.")
        else:
            messagebox.showwarning("Not Found", "No reservation found for that slot.")

    tk.Button(form, text="Reserve Slot", bg="#27ae60", fg="white",
              width=16, command=reserve).grid(row=2, column=0, pady=10)
    tk.Button(form, text="Cancel Reservation", bg="#c0392b", fg="white",
              width=20, command=cancel).grid(row=2, column=1, pady=10)

# ---------- Main Window ----------
root = tk.Tk()
root.title("Smart Dorm Map v2.2")
root.geometry("1150x750")
root.resizable(False, False)

# --- Background Image (with Pillow) ---
if os.path.exists(BACKGROUND_IMAGE):
    img = Image.open(BACKGROUND_IMAGE)
    img = img.resize((1150, 750))
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Overlay frame
overlay = tk.Frame(root, bg="#ffffff")  # solid white background
overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.9)

# Title
tk.Label(overlay, text="SMART DORM MAP",
         font=("Segoe UI", 22, "bold"),
         bg="#ffffff", fg="#2c3e50").pack(pady=8)


# --- Room Blocks ---
room_states = load_status()
buttons, counters = {}, {}

grid = tk.Frame(overlay, bg="#ffffff")
grid.pack(pady=5)

layout = [["A1", "B1"],
          ["A2", "B2"]]

for row_idx, row_blocks in enumerate(layout):
    row_frame = tk.Frame(grid, bg="#ffffff")
    row_frame.pack(pady=20)
    for col_idx, block in enumerate(row_blocks):
        frame = tk.LabelFrame(row_frame, text=f"{block} Block",
                              font=('Segoe UI', 11, 'bold'),
                              bg="white", padx=10, pady=10, relief="groove", bd=2)
        frame.grid(row=0, column=col_idx, padx=80)

        count_lbl = tk.Label(frame, text="", bg="white",
                             fg="#2980b9", font=("Segoe UI", 9, "italic"))
        count_lbl.grid(row=3, column=0, columnspan=2, pady=4)
        counters[block] = count_lbl

        for i, room in enumerate(rooms[block]):
            btn = tk.Button(frame, text=f"{room}\nAvailable",
                            bg="#27ae60", fg="white", width=18, height=2,
                            font=("Segoe UI", 9, "bold"),
                            command=lambda b=block, r=room: show_details(b, r))
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=6)
            buttons[(block, room)] = btn
            refresh_button(block, room)

# ---------- Menu Bar ----------
def reset_all():
    if messagebox.askyesno("Confirm Reset", "Reset all reservations?"):
        room_states.clear()
        save_status()
        for (b, r) in buttons:
            refresh_button(b, r)
        messagebox.showinfo("Reset", "All rooms cleared.")

def show_summary():
    info = []
    for (b, r), reservations in room_states.items():
        for s, (n, t) in reservations.items():
            info.append(f"{b}-{r}: {s} by {n}")
    messagebox.showinfo("Reservations Summary",
                        "\n".join(info) if info else "No reservations found.")

def about():
    messagebox.showinfo("About",
                        "Smart Dorm Map v2.2\nDeveloped by Team Maahnoor & Co\n"
                        "UCA Dormitory Space Monitoring Project")

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Reset All Rooms", command=reset_all)
file_menu.add_command(label="View Summary", command=show_summary)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="About", command=about)
menu.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu)

root.mainloop()

