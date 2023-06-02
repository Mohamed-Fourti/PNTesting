from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, ttk, Frame, Label, filedialog
import tkinter as tk
import paramiko
import subprocess
import os
import json


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./gui/Login_Page/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def LOGIN():

    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return canvas.create_polygon(points, **kwargs, smooth=True)

    window = Tk()

    window.geometry("930x506")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=506,
        width=930,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        469.0,
        0.0,
        1012.0,
        506.0,
        fill="#FFFFFF",
        outline="")

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        676,
        140,
        image=entry_image_2
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        676,
        290,
        image=entry_image_1
    )

    canvas.create_text(
        527.0,
        110,
        anchor="nw",
        text="Login method:",
        fill="#171435",
        font=("Black Ops One", 14 * -1)
    )

    canvas.create_text(
        517.0,
        20,
        anchor="nw",
        text="Enter your details",
        fill="#171435",
        font=("Black Ops One", 26 * -1)
    )

    rounded_background = round_rectangle(
        20.0, 17.00, 469, 491, radius=50, fill="#171435")

    canvas.create_text(
        85.0,
        77.00000000000006,
        anchor="nw",
        text="PNTesting",
        fill="#FFFFFF",
        font=("Black Ops One", 50 * -1)
    )

    canvas.create_text(
        518,
        50,
        anchor="nw",
        text="before starting, please enter the",
        fill="#808080",
        font=("Black Ops One", 16 * -1)
    )

    canvas.create_text(
        518,
        70,
        anchor="nw",
        text="information required below",
        fill="#808080",
        font=("Black Ops One", 16 * -1)
    )

    def Select_option(event):
        selected_value = event.widget.get()
        root = event.widget.winfo_toplevel()

        for child in root.winfo_children():
            if isinstance(child, Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, Text):
                        widget.destroy()
                child.destroy()

        if selected_value == "Using private key":
            new_frame = Frame(root, width=200, height=200)

            def login_with_key():
                global ssh_client

                username = username1_entry.get()
                keyfile = private_key_entry.get()
                ip_address = Ip_Address1_entry.get()

                if not os.path.isfile(keyfile):
                    tk.messagebox.showerror(
                        "Error", "SSH private key file not found")
                    return

                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                try:
                    private_key = paramiko.RSAKey.from_private_key_file(
                        keyfile)
                    ssh_client.connect(
                        ip_address, username=username, pkey=private_key)
                except Exception as e:
                    tk.messagebox.showerror(
                        "Error", "Login failed: {}".format(e))
                    return
                data = {'username': username,
                        'keyfile': keyfile, 'ip_address': ip_address}
                with open('login_credentials.json', 'w') as f:
                    json.dump(data, f)

                subprocess.Popen(
                    ['python', 'app.py', username, keyfile, ip_address])

                window.destroy()

            username1_label = Label(
                new_frame, text="Username:", font=("Black Ops One", 14 * -1))
            username1_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

            username1_entry = Entry(new_frame)
            username1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            private_key_label = Label(
                new_frame, text="Private Key:", font=("Black Ops One", 14 * -1))
            private_key_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

            private_key_entry = Entry(new_frame)
            private_key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

            Ip_Address1_label = Label(
                new_frame, text="Ip Address:", font=("Black Ops One", 14 * -1))
            Ip_Address1_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

            Ip_Address1_entry = Entry(new_frame)
            Ip_Address1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

            def browse_file():
                file_path = filedialog.askopenfilename()
                private_key_entry.delete(0, tk.END)
                private_key_entry.insert(0, file_path)

            browse_button = Button(
                new_frame, text="Browse", command=browse_file, font=("Black Ops One", 11 * -1))
            browse_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

            login_button = Button(new_frame, text="login", command=login_with_key, font=(
                "Black Ops One", 11 * -1))
            login_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

            new_frame.pack()
            new_frame.place(x=510, y=230)

        if selected_value == "Using login and password":
            new_frame = Frame(root, width=200, height=200)

            username_label = Label(
                new_frame, text="Username:", font=("Black Ops One", 14 * -1))
            username_label.grid(row=0, column=0, columnspan=2,
                                padx=5, pady=5, sticky="e")

            username_entry = Entry(new_frame)
            username_entry.grid(row=0, column=2, columnspan=2,
                                padx=5, pady=5, sticky="w")

            password_label = Label(
                new_frame, text="Password:", font=("Black Ops One", 14 * -1))
            password_label.grid(row=1, column=0, columnspan=2,
                                padx=5, pady=5, sticky="e")

            password_entry = Entry(new_frame, show="*")
            password_entry.grid(row=1, column=2, columnspan=2,
                                padx=5, pady=5, sticky="w")

            Ip_Address2_label = Label(
                new_frame, text="Ip Address:", font=("Black Ops One", 14 * -1))
            Ip_Address2_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

            Ip_Address2_entry = Entry(new_frame)
            Ip_Address2_entry.grid(row=2, column=2, padx=5, pady=5, sticky="w")
            login_button = Button(new_frame, text="login",
                                  font=("Black Ops One", 11 * -1))
            login_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")
            new_frame.pack()

            new_frame.place(x=520, y=230)

        new_frame = Frame(root, width=200, height=200)

    ComboboxSelected = ttk.Combobox(
        values=["Using private key", "Using login and password"],
        state="readonly",
        justify="center",
        font=("Black Ops One", 14 * -1)
    )
    ComboboxSelected.current(0)
    ComboboxSelected.place(
        x=555.0,
        y=133.0,
        width=250,
        height=30.0
    )
    ComboboxSelected.bind("<<ComboboxSelected>>", Select_option)

    canvas.create_text(
        90.0,
        162.00000000000006,
        anchor="nw",
        text="PNTesting is a penetration testing tool.\nSo please ensure that you have \nthe necessary permission before \nusing it to perform any testing. \nThank you!",
        fill="#FFFFFF",
        font=("Montserrat Regular", 18 * -1)
    )

    canvas.create_text(
        90.0,
        431.00000000000006,
        anchor="nw",
        text=("©") + " Mohamed Fourti, 2023",
        fill="#FFFFFF",
        font=("Black Ops One", 18 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


LOGIN()
