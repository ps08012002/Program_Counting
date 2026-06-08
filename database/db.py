import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()


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
        status
    ):

        sql = """
        INSERT INTO inspection_logs (
            username,
            image_original,
            image_result,
            count,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(
            sql,
            (
                username,
                image_original,
                image_result,
                count,
                status
            )
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def close(self):

        self.cursor.close()
        self.conn.close()