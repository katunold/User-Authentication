"""
Module for user model
"""
from database.database import DatabaseConnection
from api.utils.singleton import Singleton


class UserModel:
    """
    Model to hold user data
    """

    def __init__(self, **kwargs):
        """
        User model template
        :rtype: int
        :param user_name:
        :param email:
        :param password:
        """
        self.user_name = kwargs["user_name"]
        self.email = kwargs["email"]
        self.password = kwargs["password"]
        self.user_type = kwargs["user_type"]
        self.user_id = None


class Users(metaclass=Singleton):
    """
    Define user module attributes accessed by callers
    """

    _table_ = "user"
    _database_ = DatabaseConnection()

    def register_user(self, **kwargs) -> UserModel or None:
        """
        Register new user
        :param kwargs
        :return:
        """

        user = UserModel(user_name=kwargs["user_name"], email=kwargs["email"],
                         user_type=kwargs["user_type"], password=kwargs["password"])
        user.password = user.password.decode('utf8')
        del user.user_id
        self._database_.insert(self._table_, user.__dict__)

        return user

    def find_user_by_email(self, email) -> UserModel or None:
        """
        find a specific user given an email
        :param email:
        :return:
        """
        criteria = {'email': email}
        res = self._database_.find(self._table_, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(user_name=res['user_name'], email=res['email'], password=None, user_type=res['user_type'])
            user.user_id = res['user_id']
            return user.email
        return None

