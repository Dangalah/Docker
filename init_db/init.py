from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
import csv

def get_dada_from_csv():
    data = []
    with open('data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            data.append(tuple(row))
    return data

cnx = mysql.connector.connect(user='admin_db', password='admin_db',
                              host='db', database='db')
cursor = cnx.cursor()

DB_NAME = 'db'

TABLES = {}
TABLES['words'] = (
    "CREATE TABLE `words` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `word` varchar(14) NOT NULL,"
    "  `number` int NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

add_words = ("INSERT INTO words "
               "(word, number)"
               "VALUES (%s, %s)")

data_from_csv = get_dada_from_csv()

for k in data_from_csv:
    cursor.execute(add_words, k)

cnx.commit()

query = ("SELECT id,word,number FROM words")

cursor.execute(query)

for (id, word, number) in cursor:
  print(id, word, number)

cursor.close()
cnx.close()