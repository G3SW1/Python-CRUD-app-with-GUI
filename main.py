from AppGUI import mainGUI, loginGUI
from accounts import (
    add_user,
    add_admin,
    users,
    admins,
    load_accounts_from_files,
    save_accounts_to_files,
)


def on_app_close():
    print("APP: on_app_close, saving accounts…")
    save_accounts_to_files()


def run_app():
    print("APP: run_app from", __file__)

    # Load accounts from DATA/userAcc.txt and adminAcc.txt
    load_accounts_from_files()

    # Ensure at least one default user/admin exists
    if not users:
        add_user("jan", "heslo123")
    if not admins:
        add_admin("juraj", "tajneheslo123")

    login_result = loginGUI.create_login_window(users, admins)

    print("APP: login_result:", login_result)

    if login_result.success and login_result.role and login_result.username:
        print("APP: opening main window...")
        mainGUI.create_main_window(
            login_result.role,
            login_result.username,
            logout_callback=on_app_close,
        )
        print("APP: main window closed normally")
    else:
        print("APP: Login failed or cancelled.")
        on_app_close()


def main():
    run_app()


if __name__ == "__main__":
    main()