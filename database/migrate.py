import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inspection_logs (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) NOT NULL,

    image_original VARCHAR(255) NOT NULL,

    image_result VARCHAR(255) NOT NULL,

    count INT NOT NULL,

    status VARCHAR(10) NOT NULL,

    file_size_mb DECIMAL(10,2) NOT NULL DEFAULT 0,

    processing_time DECIMAL(10,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

cursor.close()
conn.close()

print("Migration success")