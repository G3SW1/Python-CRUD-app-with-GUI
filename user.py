
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_info(self):
        return f"Username: {self.username}, Password: {self.password}"

    def set_password(self, new_password):
        self.password = new_password

    def set_username(self, new_username):
        self.username = new_username