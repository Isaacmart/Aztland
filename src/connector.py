from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector

cnx = mysql.connector.connect(user="dbmasteruser",
                              password="_OYjz;pk$!loOqLYiMpTToo2D[>Kw|N9",
                              host="ls-0e7bba758968f544185d9f53202a36e6fd453ac0.czhp2iqbfdor.us-east-1.rds.amazonaws.com"
                              )
cursor = cnx.cursor()

DB_NAME = 'employees'

TABLES = {}

TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

cnx.close()
