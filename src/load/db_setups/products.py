import psycopg2
from contextlib import closing
from psycopg2.extras import DictCursor

with closing(psycopg2.connect(dbname='srx_qa', user='srx_qa', 
                        password='b3c6326ad2ec8457', host='localhost', port='5434')) as conn:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM srx.product LIMIT 5')
        for row in cursor:
            print(row)
