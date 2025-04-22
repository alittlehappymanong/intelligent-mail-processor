#!/usr/bin/python
import getpass
import sys
import oracledb
from pony import orm
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb
def getDB() :

    db = orm.Database()

    un = 'C##HOMEUSER'
    cs = 'localhost:1521/free'
    # pw = getpass.getpass(f'Enter password for {un}@{cs}: ')
    pw = 'password'
    db.bind(provider='oracle', user=un, password=pw, dsn=cs)
    
    return db