from typing import Optional
from user import User
from admin import Admin

def find_user_by_login(
    username: str,
    password: str,
    role: str,
    users: list[User],
    admins: list[Admin],
) -> Optional[User]:
    print("AUTH: searching", repr(username), repr(password), "role:", role)

    if role == "admin":
        for admin in admins:
            print("AUTH: checking admin:", admin.username, admin.password)
            if admin.username == username and admin.password == password:
                print("AUTH: found admin", admin.username)
                return admin
        print("AUTH: no matching admin found")
        return None

    if role == "user":
        for user in users:
            print("AUTH: checking user:", user.username, user.password)
            if user.username == username and user.password == password:
                print("AUTH: found user", user.username)
                return user
        print("AUTH: no matching user found")
        return None

    print("AUTH: unknown role", role)
    return None