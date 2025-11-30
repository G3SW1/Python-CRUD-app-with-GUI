import tkinter as gui
from tkinter import messagebox
from .loginGUI import save_login, create_login_window  # as needed
from .entryGUI import entryAdd, entryEdit, entryDelete, entryView
from .showLogsGUI import logSelect                        # whatever you use

def create_main_window(role: str, username: str | None = None, logout_callback=None):
    print("MAIN GUI: create_main_window", role, username)
    mainWindow = gui.Tk()
    mainWindow.title("Správa skladu")
    mainWindow.geometry("500x500")

    def do_logout():
        # Only log if we actually know role & username
        if role in ("admin", "user") and username:
            try:
                save_login(role, username, action="logout")
            except Exception as e:
                # Avoid crashing on logout logging
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

    #def open_log_select():
        #logSelect(mainWindow)

    # Handle window close (X button)
    mainWindow.protocol("WM_DELETE_WINDOW", on_close)

    if role == "admin":
        welcome_text = (
            f"Aplikácia na správu skladu (Admin {username})"
            if username else "Aplikácia na správu skladu (Admin)"
        )
        welcome_label = gui.Label(mainWindow, text=welcome_text)
        welcome_label.place(relx=0.1, rely=0.1)

        button1 = gui.Button(mainWindow, text="Zobraziť skladové položky", command=entryView)
        button1.place(relx=0.1, rely=0.2)

        button2 = gui.Button(mainWindow, text="Pridať novú položku", command=entryAdd)
        button2.place(relx=0.1, rely=0.3)

        button3 = gui.Button(mainWindow, text="Odstrániť položku", command=entryDelete)
        button3.place(relx=0.1, rely=0.4)

        button4 = gui.Button(mainWindow, text="Upraviť položku" ,command=entryEdit)
        button4.place(relx=0.1, rely=0.5)

        button5 = gui.Button(mainWindow, text="Spravovať používateľov")
        button5.place(relx=0.1, rely=0.6)

        button6 = gui.Button(mainWindow, text="História prihlásení", command=logSelect)
        button6.place(relx=0.1, rely=0.7)

        button7 = gui.Button(mainWindow, text="Odhlásiť sa", command=on_logout)
        button7.place(relx=0.1, rely=0.8)

    elif role == "user":
        welcome_text = (
            f"Aplikácia na správu skladu (Používateľ {username})"
            if username else "Aplikácia na správu skladu (Používateľ)"
        )
        welcome_label = gui.Label(mainWindow, text=welcome_text)
        welcome_label.place(relx=0.1, rely=0.1)

        button1 = gui.Button(mainWindow, text="Zobraziť skladové položky")
        button1.place(relx=0.1, rely=0.2)

        button2 = gui.Button(mainWindow, text="Odhlásiť sa", command=on_logout)
        button2.place(relx=0.1, rely=0.3)

    else:
        welcome_label = gui.Label(mainWindow, text="Neznáma rola", fg="red")
        welcome_label.place(relx=0.1, rely=0.1)

    mainWindow.mainloop()







