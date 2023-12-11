import unittest
from final import User, Group, UserManager
import os

import io
import sys

class TestUserStringRepresentation(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user", 1001, 1001, "Test user", "/home/test_user", "/bin/bash")

    def test_str(self):
        self.assertEqual(
            str(self.user),
            "test_user:x:1001:1001:Test user:/home/test_user:/bin/bash",
            "Incorrect string representation of User.",
        )

class TestUserWriteToFile(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()

        self.user = User("test_user", 1001, 1001, "Test user", "/home/test_user", "/bin/bash")

    def tearDown(self):
        os.remove(self.users_filename)

    def test_write_to_file(self):
        self.user.write_to_file(self.users_filename)
        with open(self.users_filename, "r") as file:
            self.assertEqual(
                file.read().strip("\n"),
                str(self.user),
                "Failed to write user information to file.",
            )

class TestGroupStringRepresentation(unittest.TestCase):
    def setUp(self):
        self.groups_filename = "groups.txt"
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.group = Group("test_group", 7000, ["test_user"])

    def tearDown(self):
        os.remove(self.groups_filename)

    def test_str(self):
        self.assertEqual(
            str(self.group),
            "test_group:x:7000:test_user",
            "Incorrect string representation of Group.",
        )

class TestGroupWriteToFile(unittest.TestCase):
    def setUp(self):
        self.groups_filename = "groups.txt"
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.group = Group("test_group", 7000, ["test_user"])

    def tearDown(self):
        os.remove(self.groups_filename)

    def test_write_to_file(self):
        self.group.write_to_file(self.groups_filename)
        with open(self.groups_filename, "r") as file:
            self.assertEqual(
                file.read().strip("\n"),
                str(self.group),
                "Failed to write group information to file.",
            )


class TestUserManagerCreateUser(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_create_user(self):
        user = User("test_user", 7000, 7000, "Test User", "/home/test_user", "/bin/bash")
        self.user_manager.create_user(user)
        with open(self.users_filename, "r") as file:
            self.assertEqual(
                file.read().strip("\n"),
                "test_user:x:7000:7000:Test User:/home/test_user:/bin/bash",
                "Failed to create user.",
            )

class TestUserManagerCreateGroup(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_create_group(self):
        group = Group("test_group", 7000, ["test_user"])
        self.user_manager.create_group(group)
        with open(self.groups_filename, "r") as file:
            self.assertEqual(
                file.read().strip("\n"),
                "test_group:x:7000:test_user",
                "Failed to create group.",
            )

class TestUserManagerAddUserToGroup(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_add_user_to_group(self):
        user = User("test_user", 7000, 7000, "Test User", "/home/test_user", "/bin/bash")
        self.user_manager.create_user(user)

        group = Group("test_group", 7000, ["test_user"])
        self.user_manager.create_group(group)


        with open(self.groups_filename, "r") as file:
            self.assertEqual(
                file.read().strip("\n"),
                "test_group:x:7000:test_user",
                "Failed to add user to group.",
            )

class TestUserManagerCatPasswd(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_cat_passwd(self):
        user = User("test_user", 7000, 7000, "Test User", "/home/test_user", "/bin/bash")
        self.user_manager.create_user(user)

        # Redirect stdout to a buffer
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.user_manager.cat_passwd()
            # Get the printed output
            printed_output = captured_output.getvalue().strip()
        finally:
            # Reset redirect.
            sys.stdout = sys.__stdout__

        # Define your expected output here
        expected_output = 'test_user:x:7000:7000:Test User:/home/test_user:/bin/bash'

        # Compare the actual and expected output
        self.assertEqual(printed_output, expected_output, "cat_passwd() did not print the correct output.")


class TestUserManagerCatGroup(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_cat_group(self):
        group = Group("test_group", 7000, ["test_user"])
        self.user_manager.create_group(group)

        # Redirect stdout to a buffer
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.user_manager.cat_group()
            # Get the printed output
            printed_output = captured_output.getvalue().strip()
        finally:
            # Reset redirect.
            sys.stdout = sys.__stdout__

        # Define your expected output here
        expected_output = 'test_group:x:7000:test_user'

        # Compare the actual and expected output
        self.assertEqual(printed_output, expected_output, "cat_group() did not print the correct output.")

class TestUserManagerIdCommand(unittest.TestCase):
    def setUp(self):
        self.users_filename = "users.txt"
        self.groups_filename = "groups.txt"

        if not os.path.exists(self.users_filename):
            open(self.users_filename, "w").close()
        if not os.path.exists(self.groups_filename):
            open(self.groups_filename, "w").close()

        self.user_manager = UserManager(self.users_filename, self.groups_filename)

    def tearDown(self):
        os.remove(self.users_filename)
        os.remove(self.groups_filename)

    def test_id_command(self):
        user = User("test_user", 7000, 7000, "Test User", "/home/test_user", "/bin/bash")
        self.user_manager.create_user(user)
        
        # Redirect stdout to a buffer
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.user_manager.id_command("test_user")
            # Get the printed output
            printed_output = captured_output.getvalue().strip()
        finally:
            # Reset redirect.
            sys.stdout = sys.__stdout__

        # Define your expected output here
        expected_output = 'uid=7000(test_user) gid=7000(test_user) groups=7000(test_user)'

        # Compare the actual and expected output
        self.assertEqual(printed_output, expected_output, "id_command() did not print the correct output.")

if __name__ == "__main__":
    unittest.main()
