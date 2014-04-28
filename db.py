import MySQLdb
import MySQLdb.cursors

class MySQLConnect(object):

  db = None

  def __init__(self, host, database, user, password):
    connection =  MySQLdb.connect(
      host=host,
      db=database,
      user=user,
      passwd=password,
      cursorclass=MySQLdb.cursors.DictCursor
    )
    self.db = connection.cursor()

  def select(self,sql):
    self.db.execute(sql)
    return self.db.fetchall()

  def close(self):
    self.db.close()

  def info(self):
    return self.db.info()
