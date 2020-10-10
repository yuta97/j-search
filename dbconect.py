import mysql.connector as mysql

def dbConnection():
    user_name = "user"
    password = "password"
    host = "mysql_db"  
    database_name = "employees"
    return   mysql.connect(
        host="mysql_db_j",
        user="user",
        passwd="password",
        port=3306,
        database="employees"
    )