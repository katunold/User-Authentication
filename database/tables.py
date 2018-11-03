"""
Module to handle schema and table creation
"""


class SchemasTables:
    """
    Class contains methods to generate tables and schemas for production and testing
    """

    @staticmethod
    def create_production_tables(cursor):
        cursor.execute("""CREATE SCHEMA IF NOT EXISTS production""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS production.user
                                       (user_id SERIAL NOT NULL PRIMARY KEY,
                                        user_name character varying(255) NOT NULL,
                                        email character varying(255) NOT NULL UNIQUE,
                                        user_type character varying(50) NOT NULL,  
                                        password character varying(255) NOT NULL);""")

    @staticmethod
    def create_test_tables(cursor):
        cursor.execute("""CREATE SCHEMA IF NOT EXISTS test""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS test.user
                                        (user_id SERIAL NOT NULL PRIMARY KEY,
                                         user_name character varying(255) NOT NULL,
                                         email character varying(255) NOT NULL UNIQUE,
                                         user_type character varying(50) NOT NULL,  
                                         password character varying(255) NOT NULL);""")