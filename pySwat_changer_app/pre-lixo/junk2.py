# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 22:19:28 2018

@author: david
"""
import sqlite3
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        conn.close()    
    except Error as e:
        print(e)
    
def query_create(query,dbfile):
    conn = sqlite3.connect(db_file)
    conn = sqlite3.connect('clientes.db')    
    cursor = conn.cursor()
    cursor.execute(query)
        
    print('concluido')
    conn.close()
    
query1 = """
CREATE TABLE clientes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cpf     VARCHAR(11) NOT NULL,
        email TEXT NOT NULL,
        fone TEXT,
        cidade TEXT,
        uf VARCHAR(2) NOT NULL,
        criado_em DATE NOT NULL
);
"""
query2 = """
SELECT* FROM  clientes
"""

 
if __name__ == '__main__':
    db_file = r"C:\Users\david\Desktop\pythonsqlite.db"
    create_connection(db_file)
    result = query_create(query1,db_file)
    
    