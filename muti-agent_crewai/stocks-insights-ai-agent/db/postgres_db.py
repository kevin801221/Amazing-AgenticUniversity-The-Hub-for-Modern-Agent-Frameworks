import psycopg2
from psycopg2 import sql, OperationalError
from utils.logger import logger

class PostgresDBClient:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, database, user, password, port=5432):
        if not hasattr(self, "_initialized"):
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.connection = None
            self._initialized = True

    def connect(self):
        """Establish a database connection."""
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                logger.info("PostgreSQL connection established.")
            except OperationalError as e:
                logger.error(f"Error connecting to PostgreSQL: {e}")
                raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("PostgreSQL connection closed.")

    def execute_query(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            # logger.info("Query executed successfully.")
            cursor.close()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def fetch_query(self, query, params=None):
        """Execute a SELECT query and fetch results."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            cursor.close()
            return results, columns
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise

    # CRUD Methods
    def create(self, table, data):
        """Insert a row into a table."""
        try:
            columns = data.keys()
            values = tuple(data.values())
            query = sql.SQL(
                "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
            ).format(
                table=sql.Identifier(table),
                fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
            )
            self.execute_query(query, values)
        except Exception as e:
            logger.error(f"Error in CREATE operation: {e}")
            raise

    def read(self, table, conditions=None):
        """Read rows from a table."""
        try:
            query = sql.SQL("SELECT * FROM {table}").format(
                table=sql.Identifier(table)
            )
            if conditions:
                condition_clause = sql.SQL(" WHERE {conditions}").format(
                    conditions=sql.SQL(" AND ").join(
                        [sql.SQL(f"{key} = %s") for key in conditions.keys()]
                    )
                )
                query += condition_clause
                params = tuple(conditions.values())
            else:
                params = None

            return self.fetch_query(query, params)
        except Exception as e:
            logger.error(f"Error in READ operation: {e}")
            raise

    def update(self, table, data, conditions):
        """Update rows in a table."""
        try:
            set_clause = sql.SQL(", ").join(
                [sql.SQL(f"{key} = %s") for key in data.keys()]
            )
            condition_clause = sql.SQL(" AND ").join(
                [sql.SQL(f"{key} = %s") for key in conditions.keys()]
            )
            query = sql.SQL(
                "UPDATE {table} SET {set_clause} WHERE {condition_clause}"
            ).format(
                table=sql.Identifier(table),
                set_clause=set_clause,
                condition_clause=condition_clause,
            )
            params = tuple(data.values()) + tuple(conditions.values())
            self.execute_query(query, params)
        except Exception as e:
            logger.error(f"Error in UPDATE operation: {e}")
            raise

    def delete(self, table, conditions):
        """Delete rows from a table."""
        try:
            condition_clause = sql.SQL(" AND ").join(
                [sql.SQL(f"{key} = %s") for key in conditions.keys()]
            )
            query = sql.SQL("DELETE FROM {table} WHERE {condition_clause}").format(
                table=sql.Identifier(table),
                condition_clause=condition_clause,
            )
            params = tuple(conditions.values())
            self.execute_query(query, params)
        except Exception as e:
            logger.error(f"Error in DELETE operation: {e}")
            raise
