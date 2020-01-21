import sqlite3
from sqlite3 import Error as sqliteError
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

    # This dictionary holds all queries needed to run db
    SET_UP_SQL = dict(
        SQL_CREATE_TABLE_CITIES="""CREATE TABLE IF NOT EXISTS cities(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                commune_name text NOT NULL,
                                district_name text NOT NULL,
                                province_name text NOT NULL);""",

        SQL_CREATE_TABLE_STATIONS="""CREATE TABLE IF NOT EXISTS stations(
                                  id integer PRIMARY KEY,
                                  name text NOT NULL,
                                  latitude text NOT NULL,
                                  longitude text NOT NULL,
                                  city integer NOT NULL REFERENCES cities(id) ON UPDATE CASCADE,
                                  address text NOT NULL);""",

        SQL_CREATE_TABLE_PARAMS="""CREATE TABLE IF NOT EXISTS params(
                                code text PRIMARY KEY,
                                name text NOT NULL,
                                formula text NOT NULL
                                );""",

        SQL_CREATE_TABLE_SENSORS="""CREATE TABLE IF NOT EXISTS sensors(
                                 id integer PRIMARY KEY,
                                 station_id integer NOT NULL REFERENCES stations(id) ON UPDATE CASCADE,
                                 param integer NOT NULL REFERENCES params(code) ON UPDATE CASCADE);""",

        SQL_CREATE_TABLE_DATA="""CREATE TABLE IF NOT EXISTS data(
                              sensor_id integer REFERENCES sensors(id) ON UPDATE CASCADE,
                              param_code text REFERENCES params(code) ON UPDATE CASCADE,
                              date integer NOT NULL,
                              value text);""",

        SQL_CREATE_TABLE_REQUEST_HISTORY="""CREATE TABLE IF NOT EXISTS request_history(
                              id integer PRIMARY KEY,
                              endpoint text NOT NULL,
                              timestamp int NOT NULL);""",

        SQL_INSERT_ALL_PARAMS="""INSERT OR REPLACE INTO params (code, name, formula) VALUES 
                            ("C6H6", "benzen", "C6H6"),
                            ("CO", "tlenek węgla", "CO"),
                            ("NO2", "dwutlenek azotu", "NO2"),
                            ("PM10", "pył zawieszony PM10", "PM10"),
                            ("PM2.5", "pył zawieszony PM2.5", "PM2.5"),
                            ("O3", "ozon", "O3"),
                            ("SO2", "dwutlenek siarki", "SO2")
                            ;""")

    def __init__(self):
        try:
            connection = sqlite3.connect(self.DB_PATH)
            self.connection = connection  # If everything went ok => set instance variable
            self.__set_up()  # Create all needed tables.
        except sqliteError as e:
            raise DbManagerError("Database failed to initialize") from e

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
            elif len(data) == 1:
                cursor.execute(sql, data[0])
            else:
                cursor.executemany(sql, data)
            self.connection.commit()
        except sqliteError as e:
            raise DbManagerError("Error when performing sql insert query") from e

    def run_sql_select(self, sql, data=None):
        """
        Runs SQLite select query. Returns data via fetchall method. Can be used for parametrized queries.

        :param sql: str
        :param data: any
        :return: list
        """
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
        for sql in self.SET_UP_SQL.values():
            self.run_sql(sql)

    def insert_from_list(self, table_name, data, replace=False):
        """
        Inserts data from a list of tuple(s). Use replace=True to use SQL's INSERT OR REPLACE. Does not return anything

        :param table_name: str
        :param data: list
        :param replace: bool
        """
        replace = "" if not replace else "OR REPLACE"
        # generate question marks with commas and delete last comma
        values_placeholders = (len(data[0]) * "?,")[:-1]
        # reformat the data to the list of tuples
        query = f"INSERT {replace} INTO {table_name} VALUES ({values_placeholders})"
        self.run_sql(query, data)

    def insert_request_into_history(self, endpoint):
        """
        Inserts specified endpoint into history with current timestamp. Does not return anything.
        :param endpoint: str
        """
        timestamp = int(datetime.datetime.now().timestamp())
        sql = f"INSERT INTO request_history (endpoint, timestamp) VALUES (?,?)"
        self.run_sql(sql, (endpoint, timestamp))

    def get_last_request(self, endpoint):
        """
        Looks into request history and returns last request and it's timestamp if found, otherwise None.

        :param endpoint: str
        :return: any
        """
        sql = "SELECT timestamp, endpoint from request_history WHERE endpoint=? ORDER BY id DESC LIMIT 1"
        data = (endpoint,)
        res = self.run_sql_select(sql, data)
        return None if len(res) == 0 else res[0]


if __name__ == "__main__":
    db = DbManager.get_instance()
    result = db.get_last_request("/station/findAll/")
    print("X")
