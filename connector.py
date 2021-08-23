import mysql.connector

cnx = mysql.connector.connect(user="dbmasteruser",
                              password="_OYjz;pk$!loOqLYiMpTToo2D[>Kw|N9",
                              host="ls-0e7bba758968f544185d9f53202a36e6fd453ac0.czhp2iqbfdor.us-east-1.rds.amazonaws.com"
                              )
print(cnx)

cnx.close()
