import tkinter as gui
from tkinter import messagebox
from accounts import add_user, add_admin, delete_user, delete_admin, users, admins


def manageAccounts():
    win = gui.Toplevel()
    win.title("Správa účtov")
    win.geometry("400x400")

    gui.Button(win, text="Pridať používateľa", command=lambda: addUser(win)).place(
        relx=0.1, rely=0.1
    )
    gui.Button(win, text="Vymazať používateľa", command=lambda: delUser(win)).place(
        relx=0.1, rely=0.2
    )
    gui.Button(win, text="Pridať administrátora", command=lambda: addAdmin(win)).place(
        relx=0.1, rely=0.3
    )
    gui.Button(win, text="Vymazať administrátora", command=lambda: delAdmin(win)).place(
        relx=0.1, rely=0.4
    )


def addUser(parent):
    win = gui.Toplevel(parent)
    win.title("Pridať používateľa")
    win.geometry("300x200")

    gui.Label(win, text="Meno používateľa:").place(relx=0.1, rely=0.1)
    nameEntry = gui.Entry(win)
    nameEntry.place(relx=0.1, rely=0.2)

    gui.Label(win, text="Heslo:").place(relx=0.1, rely=0.3)
    passwordEntry = gui.Entry(win, show="*")
    passwordEntry.place(relx=0.1, rely=0.4)

    def on_add():
        name = nameEntry.get().strip()
        pwd = passwordEntry.get().strip()
        if not name or not pwd:
            messagebox.showerror("Chyba", "Meno a heslo sú povinné.")
            return
        add_user(name, pwd)
        messagebox.showinfo("OK", "Používateľ pridaný.")
        win.destroy()

    gui.Button(win, text="Pridať", command=on_add).place(relx=0.1, rely=0.5)


def addAdmin(parent):
    win = gui.Toplevel(parent)
    win.title("Pridať administrátora")
    win.geometry("300x200")

    gui.Label(win, text="Meno správcu:").place(relx=0.1, rely=0.1)
    nameEntry = gui.Entry(win)
    nameEntry.place(relx=0.1, rely=0.2)

    gui.Label(win, text="Heslo:").place(relx=0.1, rely=0.3)
    passwordEntry = gui.Entry(win, show="*")
    passwordEntry.place(relx=0.1, rely=0.4)

    def on_add():
        name = nameEntry.get().strip()
        pwd = passwordEntry.get().strip()
        if not name or not pwd:
            messagebox.showerror("Chyba", "Meno a heslo sú povinné.")
            return
        add_admin(name, pwd)
        messagebox.showinfo("OK", "Admin pridaný.")
        win.destroy()

    gui.Button(win, text="Pridať", command=on_add).place(relx=0.1, rely=0.5)


def delUser(parent):
    win = gui.Toplevel(parent)
    win.title("Vymazať používateľa")
    win.geometry("400x400")

    gui.Label(win, text="Používatelia").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def refresh():
        # Clear old rows (keep header row 0)
        for widget in win.grid_slaves():
            if int(widget.grid_info().get("row", 1)) > 0:
                widget.destroy()

        if not users:
            gui.Label(win, text="Žiadni používatelia.", fg="gray").grid(
                row=1, column=0, padx=10, pady=5, sticky="w"
            )
            return

        for idx, u in enumerate(users):
            row = idx + 1
            gui.Label(win, text=u.username).grid(row=row, column=0, padx=10, pady=2, sticky="w")

            def make_delete_handler(username=u.username):
                def handler():
                    if delete_user(username):
                        messagebox.showinfo("OK", f"Používateľ '{username}' vymazaný.")
                        refresh()
                    else:
                        messagebox.showerror("Chyba", f"Používateľ '{username}' neexistuje.")

                return handler

            gui.Button(win, text="Vymazať", command=make_delete_handler()).grid(
                row=row, column=1, padx=10, pady=2
            )

    refresh()


def delAdmin(parent):
    win = gui.Toplevel(parent)
    win.title("Vymazať administrátora")
    win.geometry("400x400")

    gui.Label(win, text="Administrátori").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def refresh():
        # Clear old rows (keep header row 0)
        for widget in win.grid_slaves():
            if int(widget.grid_info().get("row", 1)) > 0:
                widget.destroy()

        if not admins:
            gui.Label(win, text="Žiadni administrátori.", fg="gray").grid(
                row=1, column=0, padx=10, pady=5, sticky="w"
            )
            return

        for idx, a in enumerate(admins):
            row = idx + 1
            gui.Label(win, text=a.username).grid(row=row, column=0, padx=10, pady=2, sticky="w")

            def make_delete_handler(username=a.username):
                def handler():
                    if delete_admin(username):
                        messagebox.showinfo("OK", f"Admin '{username}' vymazaný.")
                        refresh()
                    else:
                        messagebox.showerror("Chyba", f"Admin '{username}' neexistuje.")

                return handler

            gui.Button(win, text="Vymazať", command=make_delete_handler()).grid(
                row=row, column=1, padx=10, pady=2
            )

    refresh()