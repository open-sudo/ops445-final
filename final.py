import sys

class User:
    def __init__(self, username: str, uid: int, gid: int, full_name: str, home_directory: str, shell: str):
        self.username = username
        self.uid = uid
        self.gid = gid
        self.full_name = full_name
        self.home_directory = home_directory
        self.shell = shell
    
     # Method that converts this user to a string.
    def __str__(self) -> str:
        ...
    
    # Method that writes the string representation of the user at the end of the user's file. 
    def write_to_file(self, filename):
       ...

class Group:
    def __init__(self, group_name: str, gid: int, members: list =None):
        self.group_name = group_name
        self.gid = gid
        self.members = members or []

    def __str__(self) -> str:
       ...
    
    # Method that writes the string representation of the group at the end of the group's file.
    def write_to_file(self, filename: str):
       ...

class UserManager:
    def __init__(self, users_filename: str, groups_filename: str):
        self.users_filename = users_filename
        self.groups_filename = groups_filename

        # Create both files if they don't exist
        open(self.users_filename, 'a').close()
        open(self.groups_filename, 'a').close()

    def create_user(self, user: User):
        with open(self.users_filename, 'r') as file:
            existing_users = file.read().splitlines()
            for existing_user in existing_users:
                if existing_user.startswith(user.username + ":"):
                    print(f"Error: User '{user.username}' already exists.")
                    return
                elif existing_user.split(":")[2] == str(user.uid):
                    print(f"Error: UID '{user.uid}' already exists.")
                    return

        user.write_to_file(self.users_filename)
        print(f"User '{user.username}' created successfully.")

    def create_group(self, group: Group):
        with open(self.groups_filename, 'r') as file:
            existing_groups = file.read().splitlines()
            for existing_group in existing_groups:
                if existing_group.startswith(group.group_name + ":"):
                    print(f"Error: Group '{group.group_name}' already exists.")
                    return
                elif existing_group.split(":")[2] == str(group.gid):
                    print(f"Error: GID '{group.gid}' already exists.")
                    return

        group.write_to_file(self.groups_filename)
        print(f"Group '{group.group_name}' created successfully.")

    def add_user_to_group(self, username: str, group_name: str):
        with open(self.groups_filename, 'r') as file:
            existing_groups = file.read().splitlines()
            group_found = False
            for existing_group in existing_groups:
                if existing_group.startswith(group_name + ":"):
                    group_fields = existing_group.split(":")
                    gid = group_fields[2]
                    members = group_fields[3].split(",") if group_fields[3] else []

                    if username not in members:
                        members.append(username)
                        updated_group = Group(group_name, gid, members)
                        # Update the group in the file
                        with open(self.groups_filename, 'w') as group_file:
                            for g in existing_groups:
                                if g.startswith(group_name + ":"):
                                    group_file.write(str(updated_group) + '\n')
                                else:
                                    group_file.write(g + '\n')
                        print(f"User '{username}' added to group '{group_name}' successfully.")
                    else:
                        print(f"Error: User '{username}' is already a member of group '{group_name}'.")
                    group_found = True
                    break

            if not group_found:
                print(f"Error: Group '{group_name}' not found.")

    def cat_passwd(self):
       ...

    def cat_group(self):
        ...


    # Methods for the id command
    def find_user(self, username: str) -> User:
        with open(self.users_filename, 'r') as file:
            for line in file:
                if line.startswith(username + ":"):
                    user_fields = line.strip().split(":")
                    username, uid, gid, full_name, home_directory, shell = user_fields[0], int(user_fields[2]), int(user_fields[3]), user_fields[4], user_fields[5], user_fields[6]
                    return User(
                        username=username,
                        uid=uid,
                        gid=gid,
                        full_name=full_name,
                        home_directory=home_directory,
                        shell=shell
                    )

    def read_supplementary_groups(self, username: str) -> list:
        supplementary_groups = []
        with open(self.groups_filename, 'r') as group_file:
            for group_line in group_file:
                group_fields = group_line.strip().split(":")
                if username in group_fields[3].split(","):
                    supplementary_groups.append((group_fields[0], int(group_fields[2])))
        return supplementary_groups

    def id_command(self, username: str):
        ...



if __name__ == "__main__":
    # Example Usage:
    user_manager = UserManager("passwd.txt", "group.txt")

    # Create a user
    user1 = User("test_user_1", 7001, 7001, "Test User 1", "/home/test_user_1", "/bin/bash")
    user_manager.create_user(user1)

    user2 = User("test_user_2", 8001, 8001, "Test User 2", "/home/test_user_2", "/bin/bash")
    user_manager.create_user(user2)

    # Create a group
    group1 = Group("test_group_1", 7001, [])
    group2 = Group("test_group_2", 7002, [])
    group3 = Group("test_group_3", 7003, [])
    user_manager.create_group(group1)
    user_manager.create_group(group2)
    user_manager.create_group(group3)

    # Add the user to the groups
    user_manager.add_user_to_group("test_user_1", "test_group_1")
    user_manager.add_user_to_group("test_user_1", "test_group_2")
    user_manager.add_user_to_group("test_user_2", "test_group_3")
    user_manager.add_user_to_group("test_user_1", "test_group_3")

    # Print the contents of the passwd and group files
    user_manager.cat_passwd()
    user_manager.cat_group()

    # Print the id of the user
    user_manager.id_command("test_user_1")
    user_manager.id_command("test_user_2")
