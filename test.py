#!/usr/bin/python

import psycopg2
import datetime, time

dbname = 'madlibdb'
dbuser = 'root'
dbpass = 'root'
dbhost = '127.0.0.1'

def get_dbconn(dbname, dbuser, dbhost, gp_pass):
  conn = None
  count = 1
  while conn == None:
    try:
      conn = psycopg2.connect(database=dbname, user=dbuser, host=dbhost,
                           password=gp_pass)
    except Exception, e:
      count = count + 1
      print "Trial {0}: {1}".format(count, e)
      time.sleep(1)
      conn = None

  print "Connected to ", dbname
  return conn

def execute_query(conn, st):
  cur = conn.cursor()
  print st
  cur.execute(st)
  retval = None
  try:
    retval = cur.fetchone()[0]
  except:
    pass

  cur.close()
  conn.commit()
  return retval

if __name__ == '__main__':
	conn = get_dbconn(dbname, dbuser, dbhost, dbpass)
	st = 'drop table if exists data'
	execute_query(conn,st)
	st = 'create table data(value1 float, value2 float, value3 bytea)'
	execute_query(conn,st)
        file = open('Test2.csv')
	cur = conn.cursor()
    	cur.copy_from(file,'data',sep=',',columns=('value1','value2','value3'))
	cur.close()	
	conn.commit()
	conn.close()
