from pathlib import Path
from tkinter import *
from gui.Primary_Window.sub_gui.home_GUI.gui import Home
from gui.Primary_Window.sub_gui.Port_Scanning_GUI.gui import Port_Scanning
from gui.Primary_Window.sub_gui.Brute_Force_GUI.gui import Brut_Force
from gui.Primary_Window.sub_gui.security_suggestion_GUI.gui import Security_suggestions


from ssh import create_ssh_session

ssh = create_ssh_session()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./gui/Primary_Window/assets")
    

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def handle_button_press(btn_name):
    global current_window
    if btn_name == "home":
        home_button_clicked()
        current_window = Home(window)
    elif btn_name == "Port_Scanning":
        Port_Scanning_button_clicked()
        current_window = Port_Scanning(window)
    elif btn_name == "Brut_Force":
        Brut_Force_button_clicked()
        current_window = Brut_Force(window)
    elif btn_name == "Security_suggestions":
        Security_suggestions_button_clicked()
        current_window = Security_suggestions(window)


def home_button_clicked():
    print("Home button clicked")
    canvas.itemconfig(page_navigator, text="Home")
    sidebar_navigator.place(x=0, y=133)


def Port_Scanning_button_clicked():
    print("Port Scanning button clicked")
    canvas.itemconfig(page_navigator, text="Port Scanning")
    sidebar_navigator.place(x=0, y=184)


def Brut_Force_button_clicked():
    print("Brut_Force button clicked")
    canvas.itemconfig(page_navigator, text="Brut Force")
    sidebar_navigator.place(x=0, y=232)


def Security_suggestions_button_clicked():
    print("Security_suggestions button clicked")
    canvas.itemconfig(page_navigator, text="Security suggestions")
    sidebar_navigator.place(x=0, y=280)


window = Tk()
window.title("PENtesting")
window.geometry("930x506")
window.configure(bg="#171435")


canvas = Canvas(
    window,
    bg='#171435',
    height=506,
    width=930,
    bd=1,
    highlightthickness=0,
    relief="solid"
)
canvas.place(x=0, y=0)
background_image = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    566.0,
    253.0,
    image=background_image
)

current_window = Home(window)

####### HOME BUTTON #############
home_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
home_button = Button(
    image=home_button_image,
    bg="#171435",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("home"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
home_button.place(
    x=7.35,
    y=133.0,
    width=191.0,
    height=47.0
)
#################################

####### Port_Scanning BUTTON #############
Port_Scanning_button_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
Port_Scanning_button = Button(
    image=Port_Scanning_button_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("Port_Scanning"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
Port_Scanning_button.place(
    x=11.35,
    y=184.0,
    width=191,
    height=47.0
)
#####################################

####### Brut_Force BUTTON #############
Brut_Force_image = PhotoImage(
    file=relative_to_assets("button_8.png"))
Brut_Force_button = Button(
    image=Brut_Force_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("Brut_Force"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
Brut_Force_button.place(
    x=8.0,
    y=232.0,
    width=191.146240234375,
    height=47.0
)
#####################################

####### Security_suggestions BUTTON #############
Security_suggestions_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
Security_suggestions_button = Button(
    image=Security_suggestions_image,
    borderwidth=0,
    bg="#171435",
    highlightthickness=0,
    command=lambda: handle_button_press("Security_suggestions"),
    relief="sunken",
    activebackground="#171435",
    activeforeground="#171435"
)
Security_suggestions_button.place(
    x=8.0,
    y=280.0,
    width=191.146240234375,
    height=47.0
)
#####################################


##################### Navigators ###############################

####### (i)  SIDEBAR NAVIGATOR #########
sidebar_navigator = Frame(background="#FFFFFF")
sidebar_navigator.place(x=0, y=133, height=47, width=7)
########################################

####### (ii)  PAGE NAVIGATOR ###########
page_navigator = canvas.create_text(
    251.0,
    37.0,
    anchor="nw",
    text="Home",
    fill="#171435",
    font=("Black Ops One", 26 * -1))
########################################

#################################################################


# App name
canvas.create_text(
    21.0,
    21.0,
    anchor="nw",
    text="PNTesting",
    fill="#FFFFFF",
    font=("Black Ops One", 32 * -1)
)


stdin, stdout, stderr = ssh.exec_command('whoami')
current_user = stdout.read().decode().strip()

canvas.create_text(
    750.0,
    46.0,
    anchor="nw",
    text="Hello "+current_user,
    fill="#000000",
    font=("Black Ops One", 16 * -1)
)


window.resizable(False, False)
window.mainloop()
