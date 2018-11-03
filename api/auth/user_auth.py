"""
Authentication module for JWT token
"""

import bcrypt

from api.utils.singleton import Singleton


class Authenticate(metaclass=Singleton):
    """
    Class defines method used by JWT
    """
    @staticmethod
    def hash_password(password):
        """
        method to hash password
        :param password:
        :return:
        """
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(12))
#        try:
#            return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(12))
#        except ValueError:
#            return False

#    @staticmethod
#    def verify_password(password_text, hashed):
#        """
#        verify client password with stored password
#        :param password_text:
#        :param hashed:
#        :return:
#        """
#        try:
#            return bcrypt.checkpw(password_text.encode('utf8'), hashed)
#        except ValueError:
#            return False
