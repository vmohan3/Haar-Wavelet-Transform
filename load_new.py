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
	row=0
	col=0
	cur = conn.cursor()
	num=''
	c = 'starter'
	st = "INSERT INTO Large_Dataset VALUES({0},{1},{2});"
	with open('/dev/sdi/bigdataset.csv') as file:
		while c:
			try:
				c=file.read(1)
			except EOFError:
				print "Done."
				exit(1)
			if c==' ':
				if row>21840:
					cur.execute(st.format(row,col,float(num)))
					col+=1
					num=''
			elif c=='\n':
				if row>21840:
					print str(row) + " " + str(col) + " " + str(num)
					cur.execute(st.format(row,col,float(num)))
					conn.commit()
                                	col=0
				print row
				row+=1
		                num=''	
			else:
				num+=c
	cur.close()
	conn.commit()
	conn.close()	
