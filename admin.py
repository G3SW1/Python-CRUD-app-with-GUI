from user import User

class Admin(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "admin"

    def get_info(self):
        return f"Admin - {super().get_info()}"

    def set_password(self, new_password: str):
        super().set_password(new_password)
        print(f"Admin password updated for {self.username}")

    def set_username(self, new_username: str):
        super().set_username(new_username)
        print(f"Admin username updated to {self.username}")