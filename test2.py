#!/usr/bin/python

import psycopg2
import datetime, time
import cStringIO
import csv
import sys

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

def processchunk(chunk):
	print len(chunk)

def gen_chunks(reader, chunksize=10000):
	chunk = []
	for i, line in enumerate(reader):
		if ( i % chunksize == 0 and i > 0):
			yield chunk
			del chunk [:]
		chunk.append(line)
	yield chunk

if __name__ == '__main__':	
	conn = get_dbconn(dbname, dbuser, dbhost, dbpass)
	#st = 'drop table if exists data'
	#execute_query(conn,st)
	#st = 'create table data(value1 float, value2 float, value3 varchar)'
	#execute_query(conn,st)
        #csv.field_size_limit(sys.maxsize)
	file = open('/root/datasets/a.csv')
	#for chunk in gen_chunks(file):
	#	processchunk(chunk)
	#ct=0;
	#for line in file:
	#	ct+=1
	#print ct
	#cur = conn.cursor()
	for line in file:
		val = line.split()
	#	print line
		print len(val)
		break

        print len([i for i in file])

	st = "insert into data values ({0},{1},{2})".format(val[0],val[1],val[2])
	cur.execute(st);
	
	cur.close()
	conn.commit()
	conn.close()
