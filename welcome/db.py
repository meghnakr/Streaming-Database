from welcome import connect_with_connector

class sqlConnector(object):

   engine = None

   def __init__(self):
      if sqlConnector.engine is None:
         try:
            sqlConnector.engine = connect_with_connector()

         except Exception as error:
            print("Error: engine not established {}".format(error))
         else:
            print("engine established")

      self.engine = sqlConnector.engine