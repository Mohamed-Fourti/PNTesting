from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Frame, filedialog
import paramiko
import tkinter as tk
import threading
import datetime
from ssh import create_ssh_session
import re


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
            # Display an error message
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

    stdin, stdout, stderr = ssh.exec_command('nmap -v')
    if stdout.channel.recv_exit_status() != 0:
        print("nmap is not installed")
    else:
        targets = ips_entry.get('1.0', tk.END).strip().split('\n')

        total_targets = len(targets)
        full_scan_output = ""
        for i, target in enumerate(targets):
            cmd = f"sudo nmap -sS -p 80 -T5 -v {target}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            scan_output = ""

            for line in iter(stdout.readline, ''):
                output_text.insert(tk.END, line)
                output_text.see(tk.END)
                stdout.flush()
                scan_output += line
            full_scan_output += scan_output

            output_text.insert(tk.END, "__________________\n", "center")

            start_index = scan_output.index("Nmap scan report for")
            end_index = scan_output.index("Read data files from")
            Scan_output.insert(
                tk.END, scan_output[start_index:end_index] + "__________________\n", "center")

            progress = (i + 1) / total_targets * 100
            progress_bar['value'] = progress


def save_Scan_output():
    text = Scan_output.get("1.0", tk.END)
    with open("PortScan_Result_output.txt", "w") as f:
        f.write(text)


def save_output_text():
    text = full_scan_output
    with open("PortScan_Full_output.txt", "w") as f:
        f.write(text)


def start_scan_thread():
    scan_thread = threading.Thread(target=perform_scan)
    scan_thread.start()


def Port_Scanning(parent):
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
        234.5,
        300,
        image=entry_image_2
    )
    global Scan_output
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
        text="Scan Result:",
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
        x=714.0,
        y=310.0,
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
        x=695.0,
        y=350.0,
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
