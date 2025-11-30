import tkinter as gui
from tkinter import messagebox
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent

FILENAME = _PROJECT_ROOT / "DATA" / "entries.txt"


def performAddEntry(name: str, shortName: str, quantity: int, filename: str = FILENAME) -> None:
    try:
        line = f"{name} | {shortName} | {quantity}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:
        messagebox.showerror("Chyba", f"Nepodarilo sa zapísať do súboru: {e}")


def read_entries(filename: str = FILENAME) -> list[tuple[str, str, int]]:
    entries: list[tuple[str, str, int]] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) != 3:
                    continue
                name, shortName, quantity_str = parts
                try:
                    quantity = int(quantity_str)
                except ValueError:
                    continue
                entries.append((name, shortName, quantity))
    except FileNotFoundError:
        pass
    except OSError as e:
        messagebox.showerror("Chyba", f"Nepodarilo sa načítať súbor: {e}")
    return entries


def write_entries(entries: list[tuple[str, str, int]], filename: str = FILENAME) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for name, shortName, quantity in entries:
                f.write(f"{name} | {shortName} | {quantity}\n")
    except OSError as e:
        messagebox.showerror("Chyba", f"Nepodarilo sa zapísať do súboru: {e}")


def entryAdd():
    NewEmtryWindow = gui.Toplevel()
    NewEmtryWindow.title("Pridanie nového záznamu")
    NewEmtryWindow.geometry("500x400")

    gui.Label(NewEmtryWindow, text="Názov položky:").place(relx=0.1, rely=0.1)
    Field1 = gui.Entry(NewEmtryWindow, width=40)
    Field1.place(relx=0.1, rely=0.2)

    gui.Label(NewEmtryWindow, text="Skladové označenie:").place(relx=0.1, rely=0.3)
    Field2 = gui.Entry(NewEmtryWindow, width=40)
    Field2.place(relx=0.1, rely=0.4)

    gui.Label(NewEmtryWindow, text="Počet kusov:").place(relx=0.1, rely=0.5)
    Field3 = gui.Entry(NewEmtryWindow, width=40)
    Field3.place(relx=0.1, rely=0.6)

    def on_save():
        name = Field1.get().strip()
        shortName = Field2.get().strip()
        quantity_str = Field3.get().strip()

        if not name or not shortName or not quantity_str:
            messagebox.showerror("Chyba", "Všetky polia sú povinné.")
            return

        try:
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Chyba", "Množstvo musí byť celé číslo.")
            return

        performAddEntry(name, shortName, quantity)
        messagebox.showinfo("Uložené", "Položka bola pridaná.")
        NewEmtryWindow.destroy()

    gui.Button(NewEmtryWindow, text="Uložiť", command=on_save).place(relx=0.1, rely=0.7)
    gui.Button(NewEmtryWindow, text="Zrušiť", command=NewEmtryWindow.destroy).place(
        relx=0.1, rely=0.8
    )


def entryEdit():
    entries = read_entries()
    if not entries:
        messagebox.showinfo("Info", "Žiadne záznamy na úpravu.")
        return

    win = gui.Toplevel()
    win.title("Upraviť záznamy")
    win.geometry("600x400")

    gui.Label(win, text="Názov položky").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    gui.Label(win, text="Skladové označenie").grid(row=0, column=1, padx=10, pady=5, sticky="w")
    gui.Label(win, text="Počet kusov").grid(row=0, column=2, padx=10, pady=5, sticky="w")

    for idx, (name, short, qty) in enumerate(entries):
        row = idx + 1
        gui.Label(win, text=name).grid(row=row, column=0, padx=10, pady=2, sticky="w")
        gui.Label(win, text=short).grid(row=row, column=1, padx=10, pady=2, sticky="w")
        gui.Label(win, text=str(qty)).grid(row=row, column=2, padx=10, pady=2, sticky="w")

        def make_edit_handler(i=idx):
            def handler():
                open_edit_single_entry(i)
                win.destroy()

            return handler

        gui.Button(win, text="Upraviť", command=make_edit_handler()).grid(
            row=row, column=3, padx=10, pady=2
        )


def open_edit_single_entry(index: int):
    entries = read_entries()
    if index < 0 or index >= len(entries):
        messagebox.showerror("Chyba", "Neplatný index záznamu.")
        return

    name, short, qty = entries[index]

    editWin = gui.Toplevel()
    editWin.title("Upraviť záznam")
    editWin.geometry("500x400")

    gui.Label(editWin, text="Názov položky:").place(relx=0.1, rely=0.1)
    Field1 = gui.Entry(editWin, width=40)
    Field1.place(relx=0.1, rely=0.2)
    Field1.insert(0, name)

    gui.Label(editWin, text="Skladové označenie:").place(relx=0.1, rely=0.3)
    Field2 = gui.Entry(editWin, width=40)
    Field2.place(relx=0.1, rely=0.4)
    Field2.insert(0, short)

    gui.Label(editWin, text="Počet kusov:").place(relx=0.1, rely=0.5)
    Field3 = gui.Entry(editWin, width=40)
    Field3.place(relx=0.1, rely=0.6)
    Field3.insert(0, str(qty))

    def on_edit():
        new_name = Field1.get().strip()
        new_short = Field2.get().strip()
        new_qty_str = Field3.get().strip()

        if not new_name or not new_short or not new_qty_str:
            messagebox.showerror("Chyba", "Všetky polia sú povinné.")
            return

        try:
            new_qty = int(new_qty_str)
        except ValueError:
            messagebox.showerror("Chyba", "Množstvo musí byť celé číslo.")
            return

        entries[index] = (new_name, new_short, new_qty)
        write_entries(entries)
        messagebox.showinfo("Uložené", "Záznam bol upravený.")
        editWin.destroy()

    gui.Button(editWin, text="Uložiť", command=on_edit).place(relx=0.1, rely=0.7)
    gui.Button(editWin, text="Zrušiť", command=editWin.destroy).place(relx=0.1, rely=0.8)


def entryDelete():
    entries = read_entries()
    if not entries:
        messagebox.showinfo("Info", "Žiadne záznamy na odstránenie.")
        return

    win = gui.Toplevel()
    win.title("Odstrániť záznamy")
    win.geometry("600x400")

    gui.Label(win, text="Názov položky").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    gui.Label(win, text="Skladové označenie").grid(row=0, column=1, padx=10, pady=5, sticky="w")
    gui.Label(win, text="Počet kusov").grid(row=0, column=2, padx=10, pady=5, sticky="w")

    def refresh_list():
        for widget in win.grid_slaves():
            if int(widget.grid_info().get("row", 1)) > 0:
                widget.destroy()

        current_entries = read_entries()
        for idx, (name, short, qty) in enumerate(current_entries):
            row = idx + 1
            gui.Label(win, text=name).grid(row=row, column=0, padx=10, pady=2, sticky="w")
            gui.Label(win, text=short).grid(row=row, column=1, padx=10, pady=2, sticky="w")
            gui.Label(win, text=str(qty)).grid(row=row, column=2, padx=10, pady=2, sticky="w")

            def make_delete_handler(i=idx):
                def handler():
                    do_delete(i)

                return handler

            gui.Button(win, text="Odstrániť", command=make_delete_handler()).grid(
                row=row, column=3, padx=10, pady=2
            )

    def do_delete(idx: int):
        current_entries = read_entries()
        if 0 <= idx < len(current_entries):
            del current_entries[idx]
            write_entries(current_entries)
            refresh_list()
        else:
            messagebox.showerror("Chyba", "Neplatný index záznamu.")

    refresh_list()


def entryView():
    entries = read_entries()
    if not entries:
        messagebox.showinfo("Info", "Žiadne záznamy na zobrazenie.")
        return

    win = gui.Toplevel()
    win.title("Zobraziť záznamy")
    win.geometry("600x400")

    gui.Label(win, text="Názov", font=("Arial", 10, "bold")).grid(
        row=0, column=0, padx=10, pady=5, sticky="w"
    )
    gui.Label(win, text="Skladové označenie", font=("Arial", 10, "bold")).grid(
        row=0, column=1, padx=10, pady=5, sticky="w"
    )
    gui.Label(win, text="Počet kusov", font=("Arial", 10, "bold")).grid(
        row=0, column=2, padx=10, pady=5, sticky="w"
    )

    for idx, (name, short, qty) in enumerate(entries):
        row = idx + 1
        gui.Label(win, text=name).grid(row=row, column=0, padx=10, pady=2, sticky="w")
        gui.Label(win, text=short).grid(row=row, column=1, padx=10, pady=2, sticky="w")
        gui.Label(win, text=str(qty)).grid(row=row, column=2, padx=10, pady=2, sticky="w")