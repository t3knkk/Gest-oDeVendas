import mysql.connector
from logger import log_error

class DatabaseManager:
    """Gerencia a conexão e as operações com o banco de dados MySQL."""
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except mysql.connector.Error as e:
            log_error(e)
            return False

    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, params=None):
        """Executa uma query que não retorna dados (INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            log_error(e)
            self.connection.rollback()
            return False

    def fetch_all(self, query, params=None):
        """Executa uma query e retorna todos os resultados."""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            log_error(e)
            return []

    def fetch_one(self, query, params=None):
        """Executa uma query e retorna um único resultado."""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            log_error(e)
            return None