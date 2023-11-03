from src.Data import users


class User:
    def __init__(self, u):
        self.connection = u
        for us in users:
            username = us["username"]
            password = us["password"]
            username_key = f"username:{username}"
            self.connection.hset(username_key, mapping={
                "username": username,
                "password": password
            })

    def login_user(self, username, password):
        username_key = f"username:{username}"
        stored_username = self.connection.hget(username_key, "username")
        stored_password = self.connection.hget(username_key, "password")

        if stored_username and stored_password:
            if stored_username.decode('utf-8') == username and stored_password.decode('utf-8') == password:
                print(f"User {username} logged in successfully!")
                return True
            else:
                print("Invalid username or password!")
                return False
        else:
            print("Invalid username or password!")
            return False

    def register_user(self, username, password):
        username_key = f"username:{username}"
        pipeline = self.connection.pipeline()
        pipeline.watch(username_key)

        if not pipeline.hexists(username_key, "username"):
            pipeline.multi()
            pipeline.hset(username_key, mapping={
                "username": username,
                "password": password
            })
            try:
                pipeline.execute()
                print(f"User {username} registered successfully!")
                return True
            except self.connection.exceptions.WatchError:
                print(f"Username {username} already taken by another user!")
                return False
        else:
            print(f"Username {username} already taken!")
            return False
