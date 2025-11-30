import tkinter as gui
from tkinter import messagebox
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent   # .../CRUD python/AppGUI
_PROJECT_ROOT = _THIS_DIR.parent              # .../CRUD python
DATA_DIR = _PROJECT_ROOT / "DATA"

def logSelect():
    logSelectWindow = gui.Toplevel()
    logSelectWindow.title("História prihlásení")
    logSelectWindow.geometry("400x400")

    button1 = gui.Button(
        logSelectWindow,
        text="Zobraziť históriu prihlásení Admin",
        command=showAdminLogs,
    )
    button1.place(relx=0.1, rely=0.1)

    button2 = gui.Button(
        logSelectWindow,
        text="Zobraziť históriu prihlásení Používateľ",
        command=showUserLogs,
    )
    button2.place(relx=0.1, rely=0.2)


def showUserLogs():
    logWindow = gui.Toplevel()
    logWindow.title("História prihlásení Používateľ")
    logWindow.geometry("400x400")

    text = gui.Text(logWindow, wrap="word")
    text.pack(fill="both", expand=True, padx=10, pady=10)

    filename = DATA_DIR / "user.txt"  # match save_login
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                text.insert("1.0", content)
            else:
                text.insert("1.0", "Žiadne záznamy o prihláseniach používateľa.")
    except FileNotFoundError:
        text.insert("1.0", "Súbor user.txt neexistuje.\nZatiaľ žiadne prihlásenia.")
    except OSError as e:
        messagebox.showerror("Chyba pri čítaní logu", str(e))


def showAdminLogs():
    logWindow = gui.Toplevel()
    logWindow.title("História prihlásení Admin")
    logWindow.geometry("400x400")

    text = gui.Text(logWindow, wrap="word")
    text.pack(fill="both", expand=True, padx=10, pady=10)

    filename = DATA_DIR / "admin.txt"  # match save_login
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                text.insert("1.0", content)
            else:
                text.insert("1.0", "Žiadne záznamy o prihláseniach admina.")
    except FileNotFoundError:
        text.insert("1.0", "Súbor admin.txt neexistuje.\nZatiaľ žiadne prihlásenia.")
    except OSError as e:
        messagebox.showerror("Chyba pri čítaní logu", str(e))