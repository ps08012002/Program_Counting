import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()


required_env = [
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME"
]

for env_var in required_env:

    if not os.getenv(env_var):
        raise RuntimeError(
            f"{env_var} not found in environment variables"
        )


class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        self.cursor = self.conn.cursor()

    def save_log(
        self,
        username,
        image_original,
        image_result,
        count,
        status,
        file_size_mb,
        processing_time
    ):

        self.conn.ping(
            reconnect=True,
            attempts=3,
            delay=2
        )

        sql = """
        INSERT INTO inspection_logs (
            username,
            image_original,
            image_result,
            count,
            status,
            file_size_mb,
            processing_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        try:

            self.cursor.execute(
                sql,
                (
                    username,
                    image_original,
                    image_result,
                    count,
                    status,
                    file_size_mb,
                    processing_time
                )
            )

            self.conn.commit()

            return self.cursor.lastrowid

        except Exception:

            self.conn.rollback()

            raise

    def close(self):

        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()