import os

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Frame, filedialog
import paramiko
import tkinter as tk
import threading
import datetime
from ssh import create_ssh_session
import re
import sqlite3


ssh = create_ssh_session()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Security_suggestions(parent):
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

    global button_image_1
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_file_dialog(parent),
        relief="flat"
    )
    button_1.place(
        x=500,
        y=128,
        width=120.0,
        height=35.0,
    )

    global text_area
    text_area = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    text_area.place(
        x=243,
        y=200,
        width=370,
        height=240
    )

    global entry_image_1
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    canvas.create_image(
        198,
        250,
        image=entry_image_1
    )

    global entry_image_2
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    canvas.create_image(
        170,
        300,
        image=entry_image_2
    )

    canvas.create_text(
        11.0,
        27.0,
        anchor="nw",
        text="Select the Port Scan Result File:",
        fill="#000000",
        font=("Black Ops One", 20 * -1)
    )

    global File_path
    File_path = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    File_path.place(
        x=249,
        y=131,
        width=240.0,
        height=20.0
    )

    global entry_image_3
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    canvas.create_image(
        140,
        75,
        image=entry_image_3
    )

    def open_file_dialog(parent):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Nmap scan reports", "*.txt")]
        )
        if file_path:
            scan_file(file_path)
            File_path.insert(tk.END, file_path)

    return canvas


def scan_file(file_path: Path):
    with open(file_path, "r") as f:
        report = f.read()

    hosts = []
    open_ports = []
    lines = report.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith("Nmap scan report"):
            host = lines[i].split()[-1]
            hosts.append(host)
        elif lines[i].startswith("PORT"):
            port_line = lines[i + 1]
            port = port_line.split("/")[0]
            if port not in open_ports:
                open_ports.append(port)

    recommendations = []
    for host in hosts:
        for port in open_ports:
            recommendation = get_recommendation(port)
            if recommendation:
                recommendations.append(
                    f"Suggested changes for Host {host}:\n{recommendation}")

    for recommendation in recommendations:
        text_area.insert(tk.END, recommendation+"\n")


def get_recommendation(port):
    connection = sqlite3.connect("Database\database.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT recommendation FROM recommendations WHERE port=?", (port,))
    recommendation = cursor.fetchone()
    connection.close()

    if recommendation:
        return recommendation[0]
