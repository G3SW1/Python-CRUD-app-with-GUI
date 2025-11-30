import tkinter as gui
from tkinter import messagebox

from .loginGUI import save_login
from .entryGUI import entryAdd, entryEdit, entryDelete, entryView
from .showLogsGUI import logSelect
from .userManagerGUI import manageAccounts

print("IMPORTING mainGUI from", __file__)


def create_main_window(role: str, username: str | None = None, logout_callback=None):
    print("MAIN GUI: create_main_window", role, username)

    # New root for main phase
    mainWindow = gui.Tk()
    mainWindow.title("Správa skladu")
    mainWindow.geometry("500x500")

    def do_logout():
        if role in ("admin", "user") and username:
            try:
                save_login(role, username, action="logout")
            except Exception as e:
                messagebox.showwarning("Log", f"Nepodarilo sa zapísať logout: {e}")

    def on_logout():
        print("MAIN GUI: logout clicked")
        do_logout()
        mainWindow.destroy()
        if logout_callback is not None:
            logout_callback()

    def on_close():
        print("MAIN GUI: window closed")
        do_logout()
        mainWindow.destroy()
        if logout_callback is not None:
            logout_callback()

    mainWindow.protocol("WM_DELETE_WINDOW", on_close)

    if role == "admin":
        welcome_text = (
            f"Aplikácia na správu skladu (Admin {username})"
            if username
            else "Aplikácia na správu skladu (Admin)"
        )
        gui.Label(mainWindow, text=welcome_text).place(relx=0.1, rely=0.1)

        gui.Button(mainWindow, text="Zobraziť skladové položky", command=entryView).place(
            relx=0.1, rely=0.2
        )
        gui.Button(mainWindow, text="Pridať novú položku", command=entryAdd).place(
            relx=0.1, rely=0.3
        )
        gui.Button(mainWindow, text="Odstrániť položku", command=entryDelete).place(
            relx=0.1, rely=0.4
        )
        gui.Button(mainWindow, text="Upraviť položku", command=entryEdit).place(
            relx=0.1, rely=0.5
        )
        gui.Button(mainWindow, text="Spravovať používateľov", command=manageAccounts).place(
            relx=0.1, rely=0.6
        )
        gui.Button(mainWindow, text="História prihlásení", command=logSelect).place(
            relx=0.1, rely=0.7
        )
        gui.Button(mainWindow, text="Odhlásiť sa", command=on_logout).place(
            relx=0.1, rely=0.8
        )

    elif role == "user":
        welcome_text = (
            f"Aplikácia na správu skladu (Používateľ {username})"
            if username
            else "Aplikácia na správu skladu (Používateľ)"
        )
        gui.Label(mainWindow, text=welcome_text).place(relx=0.1, rely=0.1)

        gui.Button(mainWindow, text="Zobraziť skladové položky", command=entryView).place(
            relx=0.1, rely=0.2
        )
        gui.Button(mainWindow, text="Odhlásiť sa", command=on_logout).place(
            relx=0.1, rely=0.3
        )
    else:
        gui.Label(mainWindow, text="Neznáma rola", fg="red").place(relx=0.1, rely=0.1)

    mainWindow.mainloop()