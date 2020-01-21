import sqlite3
from sqlite3 import Error as sqliteError
from sqlite3 import OperationalError
import datetime


class DbManagerError(Exception):
    pass


class DbManager:
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        """
        Implementation of singleton pattern. Use this to get instance of DbManager.
        :rtype: DbManager
        """
        if cls.__INSTANCE is None:
            cls.__INSTANCE = DbManager()
        return cls.__INSTANCE

    DB_PATH = "C:/Users/Gustaw/source/repos/air-quality-index/data.db"  # TODO: change to relative path
    SQL_SETUP_DATABASE = "PRAGMA foreign_keys = ON;"

    SQL_CREATE_TABLE_CITIES = """CREATE TABLE IF NOT EXISTS cities(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                commune_name text NOT NULL,
                                district_name text NOT NULL,
                                province_name text NOT NULL);"""

    SQL_CREATE_TABLE_STATIONS = """CREATE TABLE IF NOT EXISTS stations(
                                  id integer PRIMARY KEY,
                                  name text NOT NULL,
                                  latitude text NOT NULL,
                                  longitude text NOT NULL,
                                  city integer NOT NULL REFERENCES cities(id) ON UPDATE CASCADE,
                                  address text NOT NULL);"""

    SQL_CREATE_TABLE_PARAMS = """CREATE TABLE IF NOT EXISTS params(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                formula text NOT NULL,
                                code text NOT NULL UNIQUE);"""

    SQL_CREATE_TABLE_SENSORS = """CREATE TABLE IF NOT EXISTS sensors(
                                 id integer PRIMARY KEY,
                                 station_id integer NOT NULL REFERENCES stations(id) ON UPDATE CASCADE,
                                 param integer NOT NULL REFERENCES params(id) ON UPDATE CASCADE);"""

    SQL_CREATE_TABLE_DATA = """CREATE TABLE IF NOT EXISTS data(
                              sensor_id integer REFERENCES sensors(id) ON UPDATE CASCADE,
                              param_code text REFERENCES params(code) ON UPDATE CASCADE,
                              date integer NOT NULL,
                              value text);"""

    def __init__(self):
        connection = None
        try:
            connection = sqlite3.connect(self.DB_PATH)
        except sqliteError as e:
            raise DbManagerError("Application was unable to connect") from e
        self.connection = connection  # If everything went ok => set instance variable
        self.__set_up()  # Create all needed tables.

    def run_sql(self, sql, data=None):
        """
        Runs sql query. Does not return anything and can't be used for SELECT statement.
        Can be used for inserts also but only with parametrized queries (`?` as a placeholder).
        :type sql: str
        :type data: any
        :param sql: SQL code to run. Has to have `?` as a placeholder for INSERT queries.
        :param data: data for insert as a list of tuples.
        """
        try:
            cursor = self.connection.cursor()
            if data is None:
                cursor.execute(sql)
            elif type(data) == tuple:
                cursor.execute(sql, data)
            else:
                cursor.executemany(sql, data)
            self.connection.commit()
        except sqliteError as e:
            raise DbManagerError("Error when performing sql insert query") from e

    def run_sql_select(self, sql, data=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            return cursor.fetchall()
        except sqliteError as e:
            raise DbManagerError("Error when performing sql select query") from e

    def __set_up(self):
        """
        Runs all needed sqlite queries in order to set up the database.
        """
        self.run_sql(self.SQL_SETUP_DATABASE)
        self.run_sql(self.SQL_CREATE_TABLE_CITIES)
        self.run_sql(self.SQL_CREATE_TABLE_STATIONS)
        self.run_sql(self.SQL_CREATE_TABLE_PARAMS)
        self.run_sql(self.SQL_CREATE_TABLE_SENSORS)
        self.run_sql(self.SQL_CREATE_TABLE_DATA)

    def insert_from_list(self, table_name, data, replace=False):
        replace = "" if not replace else "OR REPLACE"
        # generate question marks with commas and delete last comma
        values_placeholders = (len(data[0]) * "?,")[:-1]
        # reformat the data to the list of tuples
        # data_to_insert = [tuple(x.values()) for x in data]
        query = f"INSERT {replace} INTO {table_name} VALUES ({values_placeholders})"
        self.run_sql(query, data)

    def insert_request_into_history(self, endpoint: str):
        timestamp = int(datetime.datetime.now().timestamp())
        sql = f"INSERT INTO request_history (endpoint, timestamp) VALUES (?,?)"
        self.run_sql(sql, (endpoint, timestamp))

    def get_last_request(self, endpoint: str):
        sql = "SELECT timestamp, endpoint from request_history WHERE endpoint=? ORDER BY id DESC LIMIT 1"
        data = (endpoint,)
        return self.run_sql_select(sql, data)[0]

if __name__ == "__main__":
    db = DbManager.get_instance()
    result = db.get_last_request("/station/findAll/")
    print("X")
