from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from ssh import create_ssh_session


ssh = create_ssh_session()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Install_nmap():
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y nmap')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    print(output)
    print(error)


def Install_hydra():
    stdin, stdout, stderr = ssh.exec_command('sudo apt-get update')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    print(output)
    print(error)

    stdin, stdout, stderr = ssh.exec_command('sudo apt-get install -y hydra')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    print(output)
    print(error)


def Home(parent):

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
    global entrybox_image
    entrybox_image = PhotoImage(file=relative_to_assets("background.png"))
    canvas.create_image(341, 210, image=entrybox_image)
    canvas.create_text(
        44.0,
        80.0,
        anchor="nw",
        text="Nmap Status :  ",
        fill="#000000",
        font=("Black Ops One", 20 * -1))

    # Check if nmap is installed
    stdin, stdout, stderr = ssh.exec_command('which nmap')
    if stdout.channel.recv_exit_status() != 0:
        global image_image_1
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            207.0,
            88.0,
            image=image_image_1
        )
        canvas.create_text(
            44.0,
            110.0,
            anchor="nw",
            text="Would you like to install Nmap Now?",
            fill="#000000",
            font=("Black Ops One", 10 * -1)
        )
        global button_image_1
        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=Install_nmap,
            relief="flat"
        )
        button_1.place(
            x=320.0,
            y=204.0,
            width=97.0,
            height=23.0
        )
    else:
        global image_image_2
        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        canvas.create_image(
            207.0,
            88.0,
            image=image_image_2)

    canvas.create_text(
        44.0,
        180.0,
        anchor="nw",
        text="Hydra Status :  ",
        fill="#000000",
        font=("Black Ops One", 20 * -1))

    # Check if Hydra is installed
    stdin, stdout, stderr = ssh.exec_command('which hydra')
    if stdout.channel.recv_exit_status() != 0:
        global image_image_3
        image_image_3 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            207.0,
            188.0,
            image=image_image_3
        )
        canvas.create_text(
            44.0,
            210.0,
            anchor="nw",
            text="Would you like to install Hydra Now?",
            fill="#000000",
            font=("Black Ops One", 10 * -1)
        )
        global button_image_2
        button_image_2 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=Install_hydra,
            relief="flat"
        )
        button_2.place(
            x=320.0,
            y=304.0,
            width=97.0,
            height=23.0
        )
    else:
        global image_image_4
        image_image_4 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        canvas.create_image(
            207.0,
            188.0,
            image=image_image_4)
