import mysql.connector as mysql
user_name = "user"
password = "password"
host = "mysql_db"  
database_name = "employees"


conn = mysql.connect(
    host="mysql_db_j",
    user="user",
    passwd="password",
    port=3306,
    database="employees"
)

conn.ping(reconnect=True)

print(conn.is_connected())
cursor = conn.cursor()
cursor.execute("use employees;")
# cursor.execute("select * from teamId2;") 
# cursor.execute("select * from winrecords;")
cursor.execute("select * from winrecords where year <= 2019 and  year >= 2017 and continuou_record <= 34 and continuou_record >= 2;") 
data = cursor.fetchall()
#  where year = 2019
# data = cursor.fetchall()
print(data)
