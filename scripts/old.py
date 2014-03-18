import psycopg2
import os


def __isTableExists__(tbl_name,conn):
    
    stmt = ''' select exists(select relname                                     
                             from pg_class                                      
                             where relname= '{tbl_name}' and relkind='r'        
                            ) as is_exists ;                                    
           '''.format(tbl_name=tbl_name)

    cursor = conn.getCursor()
    cursor.execute(stmt)
    tableExists=False
    for row in cursor:
        tableExists = row['is_exists']
    cursor.close()

    return tableExists

conn = pycopg2.connect("dbname=madlibdb user=root password=root")
print "Table '{0}' Exists: " + __isTableExists__("blah",conn)
