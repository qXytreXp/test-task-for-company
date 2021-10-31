from peewee import MySQLDatabase


mysql_db = MySQLDatabase(
    "testtask1", 
    user="root",
    password="root123passwd", 
    host="127.0.0.1", 
    port=3306
)
