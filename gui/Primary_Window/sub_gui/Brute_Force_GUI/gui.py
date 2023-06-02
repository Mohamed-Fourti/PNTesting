import tempfile
import subprocess
import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Frame, filedialog
import paramiko
import tkinter as tk
import threading
import datetime
from ssh import create_ssh_session
import re
from tempfile import NamedTemporaryFile


ssh = create_ssh_session()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


IP_PATTERN = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"


def validate_ips():
    ips = ips_entry.get('1.0', tk.END).strip().split('\n')

    for ip in ips:
        if not re.match(IP_PATTERN, ip):
            tk.messagebox.showerror("Error", f"Invalid IP address: {ip}")
            return False

    return True


def perform_scan():
    if not validate_ips():
        return
    global output_text
    global full_scan_output
    output_window = tk.Toplevel()
    output_window.title("Scan Output")
    output_text = tk.Text(output_window)
    output_text.pack(fill=tk.BOTH, expand=True)

    stdin, stdout, stderr = ssh.exec_command('which hydra')
    if stdout.channel.recv_exit_status() != 0:
        print("Hydra is not installed")
    else:
        usernames = usernames_entry.get('1.0', tk.END).strip().split('\n')
        passwords = passwords_entry.get('1.0', tk.END).strip().split('\n')
        targets = ips_entry.get('1.0', tk.END).strip().split('\n')

        total_targets = len(targets)
        full_scan_output = ""
        for i, target in enumerate(targets):
            with NamedTemporaryFile(delete=False) as password_file:
                password_file.write('\n'.join(passwords).encode())
                password_file.flush()
                with NamedTemporaryFile(delete=False) as username_file:
                    username_file.write('\n'.join(usernames).encode())
                    username_file.flush()
                    sftp = ssh.open_sftp()
                    sftp.put(username_file.name,
                             f'/tmp/{os.path.basename(username_file.name)}')
                    sftp.put(password_file.name,
                             f'/tmp/{os.path.basename(password_file.name)}')
                    sftp.close()
                    cmd = f"sudo hydra -L /tmp/{os.path.basename(username_file.name)} -P /tmp/{os.path.basename(password_file.name)} {target} ssh -t 4"
                    stdin, stdout, stderr = ssh.exec_command(cmd)

                    scan_output = ""

                    for line in iter(stdout.readline, ''):
                        output_text.insert(tk.END, line)
                        output_text.see(tk.END)
                        stdout.flush()
                        scan_output += line
                    full_scan_output += scan_output

                    output_text.insert(
                        tk.END, "\n__________________\n", "center")

                    lines_to_insert = []
                    for i, line in enumerate(scan_output.splitlines()):
                        if "[DATA] attacking" in line:
                            found = scan_output.splitlines()[i+1]
                            not_fount = scan_output.splitlines()[i]
                            login_index = found.find("login:")
                            if login_index == -1:
                                host_line = not_fount.replace(
                                    "[DATA] attacking ssh://", "").replace(":22/", "")
                                lines_to_insert.append(f"host: {host_line}")
                                lines_to_insert.append(
                                    "0 valid password found")
                            else:
                                login_line = found[login_index:]
                                host_line = not_fount.replace(
                                    "[DATA] attacking ssh://", "").replace(":22/", "")
                                password_index = login_line.find("password:")
                                password = login_line[password_index:]
                                login_line = login_line[:password_index]
                                lines_to_insert.append("[22][ssh]")
                                lines_to_insert.append(f"host: {host_line}")
                                lines_to_insert.append(f"{login_line}")
                                lines_to_insert.append(f"{password}")

                    if lines_to_insert:
                        Scan_output.insert(tk.END, '\n'.join(
                            lines_to_insert) + "\n__________________\n", "center")

                    ssh.exec_command(
                        f'rm /tmp/{os.path.basename(username_file.name)} /tmp/{os.path.basename(password_file.name)}')

                    progress = (i + 1) / total_targets * 100
                    progress_bar['value'] = progress


def save_Scan_output():
    text = Scan_output.get("1.0", tk.END)
    with open("Brutforce_Result_output.txt", "w") as f:
        f.write(text)


def save_output_text():
    text = full_scan_output
    with open("Brutforce_Full_output.txt", "w") as f:
        f.write(text)


def start_scan_thread():
    scan_thread = threading.Thread(target=perform_scan)
    scan_thread.start()


def Brut_Force(parent):
    canvas = Canvas(
        parent,
        bg="#ffffff",
        height=405,
        width=675,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=230, y=72)
    global entry_image_1
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    canvas.create_image(
        234.5,
        111.5,
        image=entry_image_1
    )

    """global Scan_output
    Scan_output = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    Scan_output.place(
        x=244,
        y=275,
        width=442.0,
        height=186.0
    )
    """

    global ips_entry
    ips_entry = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    ips_entry.place(
        x=244,
        y=131,
        width=442.0,
        height=101.0
    )

    global entry_image_2
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    canvas.create_image(
        103,
        300,
        image=entry_image_2
    )
    global entry_image_3
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    canvas.create_image(
        300.5,
        300,
        image=entry_image_3
    )
    global entry_image_4
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    canvas.create_image(
        525,
        250,
        image=entry_image_4
    )

    global usernames_entry
    usernames_entry = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    usernames_entry.place(
        x=244,
        y=275,
        width=185.0,
        height=186.0
    )

    global passwords_entry
    passwords_entry = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    passwords_entry.place(
        x=442,
        y=275,
        width=185.0,
        height=186.0
    )

    canvas.create_text(
        11.0,
        27.0,
        anchor="nw",
        text="Enter target IP addresses (one per line):",
        fill="#000000",
        font=("Black Ops One", 20 * -1)
    )

    canvas.create_text(
        11.0,
        169.0,
        anchor="nw",
        text="Usernames Lists:",
        fill="#000000",
        font=("Black Ops One", 20 * -1)
    )
    canvas.create_text(
        210.0,
        169.0,
        anchor="nw",
        text="Passwords Lists:",
        fill="#000000",
        font=("Black Ops One", 20 * -1)
    )

    global button_image_1
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=start_scan_thread,
        relief="flat"
    )
    button_1.place(
        x=740.0,
        y=140.0,
        width=120.0,
        height=33.0
    )

    global Scan_output
    Scan_output = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    Scan_output.place(
        x=665,
        y=275,
        width=180.0,
        height=90.0
    )

    global button_image_2
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=save_output_text,
        relief="flat"
    )
    button_2.place(
        x=675.0,
        y=390.0,
        width=175.0,
        height=33.0
    )

    global button_image_3
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        command=save_Scan_output,
        highlightthickness=0,
        relief="flat"
    )
    button_3.place(
        x=657.0,
        y=430.0,
        width=210.0,
        height=33.0
    )

    global progress_bar
    progress_bar = ttk.Progressbar(parent, orient='horizontal', length=200)
    progress_bar.place(
        x=735.0,
        y=180.0,
        width=130.0,
        height=33.0
    )
