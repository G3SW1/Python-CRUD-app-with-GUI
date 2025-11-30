import tkinter as gui
from tkinter import messagebox
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from authentificate import find_user_by_login
from admin import Admin
from user import User

_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent
DATA_DIR = _PROJECT_ROOT / "DATA"


@dataclass
class LoginResult:
    success: bool
    role: str | None
    username: str | None


def save_login(role: str, username: str, action: str = "login"):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = DATA_DIR / f"{role}.txt"  # DATA/user.txt or DATA/admin.txt
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{now} - {username} ({action})\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:
        messagebox.showwarning("File Save", f"Nepodarilo sa uložiť: {e}")


def create_login_window(users: list[User], admins: list[Admin]) -> LoginResult:
    success = False
    role_selected: str | None = None
    username_value: str | None = None

    root = gui.Tk()
    root.title("Výber prihlásenia")

    selection_frame = gui.Frame(root)
    selection_frame.pack(padx=10, pady=10)
    gui.Label(selection_frame, text="Vyberte rolu:", font=("Arial", 12, "bold")).pack(pady=(0, 8))

    def perform_login(role: str, username: str, password: str):
        nonlocal success, username_value, role_selected

        if not username or not password:
            messagebox.showerror("Prihlásenie", "Meno a heslo sú povinné")
            return

        print("GUI: perform_login", repr(username), repr(password), "role:", role)

        user_obj = find_user_by_login(username, password, role, users, admins)

        if user_obj is None:
            if role == "admin":
                messagebox.showerror("Prihlásenie neúspešné", "Nesprávne admin údaje")
            else:
                messagebox.showerror("Prihlásenie neúspešné", "Nesprávne používateľské údaje")
            return

        success = True
        role_selected = "admin" if isinstance(user_obj, Admin) else "user"
        username_value = user_obj.username

        print(
            "GUI: login OK; success=",
            success,
            "role_selected=",
            role_selected,
            "username_value=",
            username_value,
        )

        if role_selected == "admin":
            messagebox.showinfo("Prihlásenie", "Admin prihlásenie úspešné")
        else:
            messagebox.showinfo("Prihlásenie", "Používateľ prihlásený")

        save_login(role_selected, username_value, action="login")
        root.destroy()

    def show_login_form(role: str):
        nonlocal selection_frame, role_selected
        role_selected = role
        selection_frame.pack_forget()
        form_frame = gui.Frame(root)
        form_frame.pack(padx=10, pady=10)

        gui.Label(
            form_frame,
            text=("Admin Meno" if role == "admin" else "Používateľ Meno"),
        ).grid(row=0, column=0, sticky="w")
        username_entry = gui.Entry(form_frame)
        username_entry.grid(row=0, column=1)

        gui.Label(
            form_frame,
            text=("Admin Heslo" if role == "admin" else "Heslo"),
        ).grid(row=1, column=0, sticky="w")
        password_entry = gui.Entry(form_frame, show="*")
        password_entry.grid(row=1, column=1)

        gui.Button(
            form_frame,
            text="Prihlásiť",
            command=lambda: perform_login(role, username_entry.get(), password_entry.get()),
        ).grid(row=2, columnspan=2, pady=(8, 0))

        gui.Button(
            form_frame,
            text="Späť",
            command=lambda: (form_frame.pack_forget(), reset_to_selection()),
        ).grid(row=3, columnspan=2, pady=(4, 0))

    def reset_to_selection():
        nonlocal selection_frame, role_selected
        role_selected = None

        selection_frame = gui.Frame(root)
        selection_frame.pack(padx=10, pady=10)
        gui.Label(selection_frame, text="Vyberte rolu:", font=("Arial", 12, "bold")).pack(
            pady=(0, 8)
        )
        gui.Button(
            selection_frame, text="Používateľ", width=18, command=lambda: show_login_form("user")
        ).pack(pady=4)
        gui.Button(
            selection_frame, text="Správca", width=18, command=lambda: show_login_form("admin")
        ).pack(pady=4)

    gui.Button(selection_frame, text="Používateľ", width=18, command=lambda: show_login_form("user")).pack(
        pady=4
    )
    gui.Button(selection_frame, text="Správca", width=18, command=lambda: show_login_form("admin")).pack(
        pady=4
    )

    root.mainloop()
    print("GUI: returning LoginResult", success, role_selected, username_value)
    return LoginResult(success=success, role=role_selected, username=username_value)