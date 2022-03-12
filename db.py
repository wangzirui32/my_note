import os
import sqlite3

def conn_db(app):
   is_db_file =  os.path.isfile(app.config['DATABASE'])
   conn = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
   cursor = conn.cursor()

   if not is_db_file:
       cursor.execute('''CREATE TABLE notes
          (id INT PRIMARY KEY     NOT NULL,
          content         TEXT    NOT NULL
          );''')
       cursor.execute('''CREATE TABLE timings
          (id INT PRIMARY KEY     NOT NULL,
          timestamp       INT     NOT NULL,
          notes_id        INT     NOT NULL
          );''')
       conn.commit() 

   return DBQuery(conn)

class DBQuery():
   def __init__(self, conn):
      self.conn = conn
      self.cursor = conn.cursor()

   def select(self, CONTENT, FROM, WHERE=''):
      if WHERE:
         result = self.cursor.execute("SELECT {} FROM {} WHERE {}".format(CONTENT, FROM, WHERE))
      else:
         result = self.cursor.execute("SELECT {} FROM {}".format(CONTENT, FROM))
      return result

   def insert(self, INTO, CONTENT, VALUES):
      self.cursor.execute("""INSERT INTO {} ({}) VALUES ({})""".format(INTO, CONTENT, VALUES))
      self.conn.commit()

   def update(self, TABLE, SET, WHERE):
      self.cursor.execute("""UPDATE {} SET {} WHERE {}""".format(TABLE, SET, WHERE))
      self.conn.commit()

   def delete(self, TABLE, WHERE):
      self.cursor.execute("""DELETE FROM {} WHERE {}""".format(TABLE, WHERE))
      self.conn.commit()

   def close(self):
      self.cursor.close()
      self.conn.close()