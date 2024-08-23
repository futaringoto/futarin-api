import os
import datetime
import mysql.connector
from dotenv import load_dotenv
import mysql.connector.errorcode

load_dotenv()

db_config = {
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'host': '127.0.0.1',
    'port': '3306',
    'database': os.environ['MYSQL_DATABASE']
}

def create_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        create_table_query = '''
            CREATE TABLES texts (
                text_id INT AUTO_INCREMENT PRIMARY KEY,
                prompt TEXT NOT NULL,
                generated_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        '''

        cursor.execute(create_table_query)
        print('正常にテーブルが作成されました')

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQLの接続が閉じられました')

def insert_data(prompt: str, generated_text: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    dt_now = datetime.datetime.now()
    created_at = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')

    try:
        insert_query = f'''
            INSERT INTO texts VALUES (0, {prompt}, {generated_text}, {created_at});
        '''

        cursor.execute(insert_query)

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()