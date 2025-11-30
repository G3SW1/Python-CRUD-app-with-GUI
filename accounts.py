from pathlib import Path
from user import User
from admin import Admin

# Global in‑memory lists used by the whole app
users: list[User] = []
admins: list[Admin] = []

# --- in‑memory operations ---


def add_user(username: str, password: str) -> None:
    users.append(User(username, password))


def add_admin(username: str, password: str) -> None:
    admins.append(Admin(username, password))


def delete_user(username: str) -> bool:
    for u in list(users):
        if u.username == username:
            users.remove(u)
            return True
    return False


def delete_admin(username: str) -> bool:
    for a in list(admins):
        if a.username == username:
            admins.remove(a)
            return True
    return False


# --- persistence to DATA/userAcc.txt, DATA/adminAcc.txt ---

_THIS_DIR = Path(__file__).resolve().parent
DATA_DIR = _THIS_DIR / "DATA"
USER_ACC_FILE = DATA_DIR / "userAcc.txt"
ADMIN_ACC_FILE = DATA_DIR / "adminAcc.txt"


def load_accounts_from_files() -> None:
    """Load users/admins from text files into the global lists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    users.clear()
    admins.clear()

    # Load users
    if USER_ACC_FILE.exists():
        with USER_ACC_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) != 2:
                    continue
                username, password = parts
                users.append(User(username, password))

    # Load admins
    if ADMIN_ACC_FILE.exists():
        with ADMIN_ACC_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) != 2:
                    continue
                username, password = parts
                admins.append(Admin(username, password))


def save_accounts_to_files() -> None:
    """Overwrite account files with current users/admins."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with USER_ACC_FILE.open("w", encoding="utf-8") as f:
        for u in users:
            f.write(f"{u.username} | {u.password}\n")

    with ADMIN_ACC_FILE.open("w", encoding="utf-8") as f:
        for a in admins:
            f.write(f"{a.username} | {a.password}\n")