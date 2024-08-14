import csv

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}')"

class UserDetails:
    def __init__(self, csv_file_path):
        self.users = []
        self.load_users_from_csv(csv_file_path)
        
    def readlines(self, filename):
        with open(filename) as file:
            return file.readlines()

    def load_users_from_csv(self, csv_file_path):
        try:
            contents = self.readlines(csv_file_path)
            fields = contents.pop(0).strip().split(",")
            for i, field in enumerate(fields):
                if field.lower() == "username":
                    username_column=i
                elif field.lower() == "password":
                    password_column=i
            for row in contents:
                cells = row.strip().split(",")
                username = cells[username_column]
                password = cells[password_column]
                user = User(username, password)
                self.users.append(user)
        except FileNotFoundError:
            print(f"Error: The file '{csv_file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_users(self):
        return self.users


if __name__ == "__main__":
    csv_file_path = 'users.csv'
    user_details = UserDetails(csv_file_path)
    users = user_details.get_users()
    for user in users:
        print(user)
