import os
import pymysql

mydb, mycursor = None, None

def connect_db():
    global mydb, mycursor
    try:
        mydb = pymysql.connect(
            host=os.getenv("DATABASE_HOST", "127.0.0.1"),
            user=os.getenv("DATABASE_USER", "root"),
            password=os.getenv("DATABASE_PASSWORD", "root"),
            database=os.getenv("DATABASE_NAME", "stego"),
            autocommit=True
        )
        mycursor = mydb.cursor()
        print("✅ MySQL connection established successfully!")
        init_db(mydb, mycursor)
    except pymysql.MySQLError as err:
        print(f"❌ MySQL connection error: {err}")
        mydb, mycursor = None, None
    return mydb, mycursor


def init_db(mydb, mycursor):
    if not mycursor:
        return

    create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    create_history = """
    CREATE TABLE IF NOT EXISTS history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        original_filename VARCHAR(255),
        encoded_filename VARCHAR(255),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """

    try:
        mycursor.execute(create_users)
        mycursor.execute(create_history)
        mydb.commit()
        print("✅ Tables checked/created successfully.")
    except pymysql.MySQLError as err:
        print(f"❌ DB Init Error: {err}")
