#!/usr/bin/python

import psycopg2
import datetime,time

dbname = 'madlibdb'
dbuser = 'root'
dbpass = 'root'
dbhost = 'localhost'
size = 50000

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
  #print st
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
	st = "DROP TABLE IF EXISTS Large_Dataset"
	execute_query(conn,st)
	st = "CREATE TABLE Large_Dataset(Row int, Col int, Value float)"
	execute_query(conn,st)
	with open('/root/datasets/bigdataset.csv') as file:
		r=0
		for line in file:
			cur = conn.cursor()
			c=0
			for chunk in line.split():
				st = "INSERT INTO Large_Dataset VALUES({0},{1},{2})".format(r,c,chunk)
				if r%100==0:
					print st
				cur.execute(st)
				c+=1
			r+=1
			cur.close()
			conn.commit()
	conn.commit()
	conn.close()	
