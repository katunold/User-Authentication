"""
Module to handle all database connections
"""
import os
import psycopg2 as pg
from dotenv import load_dotenv

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor

from api.config.config import TestingConfig, DevelopmentConfig, ProductionConfig
from database.tables import SchemasTables
from api.utils.singleton import Singleton


class DatabaseConnection(metaclass=Singleton):
    """
    Database connection class
    Handles all database related issues
    """
    _conn_ = None
    schema = ProductionConfig.SCHEMA_PRODUCTION

    class DbConnection(object):
        def __init__(self, schema, app):
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            database = os.getenv("DB")
            self.create_tables = SchemasTables
            self.conn = None

            try:
                if schema == 'development':
                    self.schema = schema
                    self.conn = pg.connect(database_url,
                                           cursor_factory=RealDictCursor,
                                           options=f'-c search_path={self.schema}')
                    cur = self.conn.cursor()

                    self.create_tables.create_production_tables(cur)

                    self.conn.commit()
#                    print("Just connected to " + self.schema)
                    self.conn.autocommit = False
                else:
                    self.schema = schema
                    self.conn = pg.connect(database="authentication",
                                           user="postgres",
                                           password="qwerty",
                                           host="127.0.0.1",
                                           port="5432",
                                           cursor_factory=RealDictCursor,
                                           options=f'-c search_path={self.schema}')
                    cur = self.conn.cursor()

                    self.create_tables.create_test_tables(cur)

                    self.conn.commit()
#                    print("Just connected to " + self.schema)
                    self.conn.autocommit = False
            except pg.OperationalError:
                conn = pg.connect(user="postgres", password="qwerty", host="127.0.0.1", port="5432")
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                if app.config['TESTING']:
                    cur.execute("CREATE DATABASE %s ;" % database)
                    print('connecting to %s ...' % database)
                    conn = pg.connect(database_url,
                                      cursor_factory=RealDictCursor,
                                      options=f'-c search_path={self.schema}')
                    cur = conn.cursor()
                    print("Successfully connected")

                    self.create_tables.create_test_tables(cur)

                    conn.commit()
                    conn.close()
                    print("Successfully connected to schema "+self.schema)
                else:
                    cur.execute("CREATE DATABASE %s ;" % database)
                    print('connecting to %s ...' % database)
                    conn = pg.connect(database_url,
                                      cursor_factory=RealDictCursor,
                                      options=f'-c search_path={self.schema}')
                    cur = conn.cursor()
                    print("Successfully connected")

                    self.create_tables.create_production_tables(cur)

                    conn.commit()
                    conn.close()
                    print("Successfully connected to schema " + self.schema)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()

    def init_db(self, app):
        """
        Provides a database connection object
        :param app:
        :return:
        """
        if app.config['TESTING']:
            self.schema = TestingConfig.SCHEMA_TESTING
        else:
            self.schema = DevelopmentConfig.SCHEMA_PRODUCTION

        try:
            if not self._conn_ and app.config['TESTING']:
                self._conn_ = self.DbConnection(self.schema, app).conn
                self._conn_.autocommit = True
            else:
                self._conn_ = self.DbConnection(self.schema, app).conn
        except pg.DatabaseError as ex:
            print("Error: " + str(ex))

    def insert(self, table, data):
        """
        handle all insertions into the database
        :param table:
        :param data:
        :return:
        """
        if not table or not data or not isinstance(data, dict):
            return False
        columns = tuple(data.keys())
        values = tuple(data.values())

        _top = f"""INSERT INTO {self.schema}.{table} ("""

        cols = ", ".join([f""" "{n}" """ for n in columns])

        middle = """) VALUES ("""

        val = ", ".join([f""" '{v}' """ for v in values])

        bottom = """)"""

        sql = _top + cols + middle + val + bottom

        cur = self._conn_.cursor()
        cur.execute(sql)
        self._conn_.commit()
        if cur:
            return cur
        return None

    def find(self, name_of_table, criteria=None, join=None):
        """
        handles all queries to retrieve data
        :param name_of_table:
        :param criteria:
        :param join:
        :return:
        """
        sql = ""
        if not criteria and not join:
            sql = f"""SELECT * FROM {self.schema}.{name_of_table}"""
        else:
            if criteria and not join:
                columns = tuple(criteria.keys())
                values = tuple(criteria.values())
                top1 = f"""SELECT * FROM {self.schema}.{name_of_table} WHERE ("""

                if len(columns) == 1:
                    crit = f""" "{columns[0]}"='{values[0]}' )"""
                else:
                    crit = " AND ".join([f""" "{k}" = '{v}' """ for k, v in
                                         criteria.items()]) + """)"""

                sql = top1 + crit
            else:
                pass
        cur = self._conn_.cursor()
        cur.execute(sql)
        self._conn_.commit()
        if cur:
            val = cur.fetchall()
            if len(val) == 1:
                return val[0]
            elif len(val) > 1:
                return val
        return None

    def drop_test_schema(self):
        """
        delete test schema after using it
        :return:
        """
        cur = self._conn_.cursor()
        cur.execute("""DROP SCHEMA test CASCADE""")
#        cur.execute("""DELETE FROM test.orders""")
#        cur.execute("""DELETE FROM test.user""")
#        cur.execute("""DELETE FROM test.blacklist_token""")
        self._conn_.commit()
