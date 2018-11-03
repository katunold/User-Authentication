"""
module to handle user input validation
"""
import re

from api.models.user_model import Users


class Validators:
    """
    Class defines validator functions
    """

    user = Users()

    @staticmethod
    def validate_name(name):
        """
        Username validator
        :param name:
        :return:
        """
        username_regex = re.compile("^[A-Za-z ]{4,30}$")
        if not username_regex.match(name):
            return False
        return True

    @staticmethod
    def validate_email(email) -> bool:
        """
        Validate email address
        :param email:
        :return:
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(email):
            return False
        return True

    @staticmethod
    def validate_password(password, length) -> bool:
        """
        password validator
        :param password:
        :param length:
        :return:
        """
        if length > len(password):
            return False
        return password.isalnum()

    def check_if_email_exists(self, email):
        """
        Check if the email already exists
        :param email:
        :return:
        """
        if self.user.find_user_by_email(email):
            return False
        return True

    @staticmethod
    def validate_user_type(user_type: str):
        if user_type.lower() == "admin" or user_type.lower() == "client":
            return True
        return False
