"""
Module contains all global constants
"""


class HostConfig:
    """
    System HOST configuration settings
    They can be changed at any time.
    """
    HOST = "0.0.0.0"
    PORT = 5000


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = "126c21c31664183ab64b9ae72be7f1b1b76fe16dab652aa1"
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    SECRET_KEY = "126c21c31664183ab64b9ae72be7f1b1b76fe16dab652aa1"
    DEBUG = True
    SCHEMA_PRODUCTION = "production"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SCHEMA_TESTING = "test"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SCHEMA_PRODUCTION = "production"