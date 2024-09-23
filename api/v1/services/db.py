import mysql.connector

from v1.utils.config import get_mysql_name, get_mysql_root_pass

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password=get_mysql_root_pass(),
    database=get_mysql_name(),
)

conn.ping(reconnect=True)
