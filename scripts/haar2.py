import psycopg2
import datetime, time
import math
import numpy

dbname = 'madlibdb'
dbuser = 'root'
dbpass = 'root'
dbhost = '127.0.0.1'


data = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [0, 4, 2, 9] ]

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
  cur.execute(st)
  retval = None
  try:
    retval = cur.fetchone()[0]
  except:
    pass

  cur.close()
  conn.commit()
  return retval

def haar_matrix(matrix):
  haarCol = [[0 for x in xrange(len(matrix[0]))] for x in xrange(len(matrix))]

  for i in range(len(matrix)/2):
    for j in range(len(matrix[0])):
      if (2*i == j) or (2*i+1 == j):
        haarCol[i][j] =  math.sqrt(2)/2

  for i in range(len(matrix)/2, len(matrix)):
    for j in range(len(matrix[0])):
      k = i-len(matrix)/2
      if (2*k == j) or (2*k+1 == j):
        haarCol[i][j] = -math.sqrt(2)/2
        if j%2 != 0:
          haarCol[i][j] *= -1

  return haarCol

def user_space_threshold(encoded, threshold):
  for i in range(len(encoded)):
    for j in range(len(encoded)):
      if encoded[i][j] < threshold:
        encoded[i][j] = 0

  return encoded

def db_threshold(threshold):
  st = 'UPDATE table SET encoded = 0 WHERE '+str(threshold)+' > ANY (encoded);'

def to_postgresql_2d_array(matrix):
  out = '{'
  for i in range(len(matrix)):
    out += '{'
    for j in range(len(matrix[0])):
      out += str(matrix[i][j])
      if j != len(matrix[0])-1:
        out += ', '
    out += '}'
    if i != len(matrix)-1:
      out += ','
  out += '}'
  return out

def to_postgresql_array(matrix):
  out = '{'
  for i in range(len(matrix)):
    out += str(matrix[i])
    if i != len(matrix)-1:
      out += ','
  out += '}'
  return out

def haar_transform(matrix):
  return numpy.dot(numpy.array(haar_matrix(matrix)), numpy.array(matrix))

test_insert = """
CREATE OR REPLACE FUNCTION test_insert(in_table VARCHAR(30), out_table VARCHAR(30)) 
RETURNS void AS $$
DECLARE
	val float;
BEGIN
	EXECUTE format('CREATE TABLE %I (row int, col int, value float)', out_table);
	EXECUTE format('SELECT value FROM %I WHERE row=0 AND col=0', in_table) INTO val;
	EXECUTE format('INSERT INTO %I VALUES (0, 0, %s)', out_table, val);
END;
$$ LANGUAGE plpgsql;
"""

psql_haar = """
CREATE OR REPLACE FUNCTION haar_transform(in_table VARCHAR(30), out_table VARCHAR(30)) 
RETURNS void AS $$
DECLARE
        i int;
        j int;
        width int;
        height int;
        size int;
	half_size int;
        haar_val_1 float;
        haar_val_2 float;
	a float;
	b float;
BEGIN
	EXECUTE format('DROP TABLE IF EXISTS %I', out_table);
	EXECUTE format('CREATE TABLE %I (row int, col int, value float)', out_table);

        EXECUTE format('SELECT max(col) FROM %I', in_table) INTO width;
        EXECUTE format('SELECT max(row) FROM %I', in_table) INTO height;
        
	IF width<height THEN
                size := width+1;
        ELSE
                size := height+1;
        END IF;
	half_size := size/2;
	
	EXECUTE 'CREATE OR REPLACE TABLE temp(row integer, col integer, value double precision)';
        EXECUTE 'CREATE INDEX ON temp (row)';
        FOR i in 0..(size-1) LOOP
                EXECUTE format('INSERT INTO temp SELECT * FROM %I WHERE col=%s', in_table, i);
                FOR j in 0..(half_size-1) LOOP
			EXECUTE format('SELECT value FROM temp WHERE row=2*%s', j) INTO a;
			EXECUTE format('SELECT value FROM temp WHERE row=2*%s+1', j) INTO b;
                        haar_val_1 := compute_transform(a, b, FALSE);
                        haar_val_2 := compute_transform(a, b, TRUE);
                        EXECUTE format('INSERT INTO %I VALUES (%s, %s, %s)', out_table, j, i, haar_val_1);
                        EXECUTE format('INSERT INTO %I VALUES (%s+%s, %s, %s)', out_table, j, half_size, i, haar_val_2);
                END LOOP;
        END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION compute_transform(a float, b float, second_half boolean)
RETURNS float AS $$
DECLARE
        result float;
BEGIN
        IF second_half THEN
                result := (0-(sqrt(2)/2)*a) + (sqrt(2)/2)*b;
        ELSE
                result := (sqrt(2)/2)*a + (sqrt(2)/2)*b;
        END IF;

        return result;
END;
$$ LANGUAGE plpgsql;"""

threshold = """
CREATE OR REPLACE FUNCTION threshold(in_table VARCHAR(30), out_table VARCHAR(30), threshold float)
RETURNS VOID AS $$
BEGIN
	EXECUTE format('SELECT * FROM %I WHERE value > %s', in_table, threshold) INTO out_table;
END;
$$ LANGUAGE plpgsql;"""


if __name__ == '__main__':
	row_size = 2500
	col_size = 2500
	size = min(row_size, col_size)
	tname = 'smalldata'
	
	conn = get_dbconn(dbname, dbuser, dbhost, dbpass)
	#execute_query(conn,psql_haar)
	#execute_query(conn,test_insert)
	execute_query(conn,threshold)

