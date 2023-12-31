import yaml
import sqlalchemy


class DatabaseConnector:
    def read_db_creds(self, creds):
        """
        The function reads database credentials from a YAML file.
        """
        with open(creds, "r") as file:
            db_credentials = yaml.safe_load(file)

        return db_credentials

    def init_db_engine(self, creds):
        """
        The `init_db_engine` function initializes a database engine using the credentials read from a file
        and returns the engine.
        :return: The `self.engine` object is being returned.
        """

        creds = self.read_db_creds(creds)

        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = creds["HOST"]
        PASSWORD = creds["PASSWORD"]
        USER = creds["USER"]
        DATABASE = creds["DATABASE"]
        PORT = creds["PORT"]
        self.engine = sqlalchemy.create_engine(
            f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )
        print("Database connected")
        return self.engine

    def list_db_tables(self):
        """The code block you provided is defining a method called `list_db_tables` in the `DatabaseConnector`
        class. This method is responsible for connecting to the database, inspecting the tables in the
        database, and returning a list of table names."""
        engine = self.init_db_engine("db_creds.yaml")
        table_inspector = sqlalchemy.inspect(engine)
        tables = table_inspector.get_table_names()

        print(tables)
        return tables

    def upload_to_db(self, df, table_name):
        """
        The function `upload_to_db` uploads a pandas DataFrame to a database table using the specified table
        name.

        :param df: The parameter `df` is a pandas DataFrame that contains the data you want to upload to the
        database
        :param table_name: The `table_name` parameter is a string that specifies the name of the table in
        the database where you want to upload the DataFrame (`df`)
        """

        engine = self.init_db_engine("pgAdmin.yaml")

        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        print("Data successfully uploaded.")
