from AppGUI import mainGUI, loginGUI
from user import User
from admin import Admin

def add_user(username: str, password: str, users: list[User]) -> None:
    users.append(User(username, password))

def add_admin(username: str, password: str, admins: list[Admin]) -> None:
    admins.append(Admin(username, password))

def run_app():
    print("APP: run_app")
    users: list[User] = []
    admins: list[Admin] = []

    add_user("jan", "heslo123", users)
    add_admin("juraj", "tajneheslo123", admins)

    login_result = loginGUI.create_login_window(users, admins)

    print("APP: login_result", login_result)

    if login_result.success and login_result.role and login_result.username:
        mainGUI.create_main_window(
            login_result.role,
            login_result.username,
            logout_callback=run_app,
        )
    else:
        print("Login failed or cancelled.")

def main():
    run_app()

if __name__ == "__main__":
    main()