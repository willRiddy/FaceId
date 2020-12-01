import mysql.connector

class Insert():

    def __init__(self, table, name, photoPath=None, host='localhost', user='will', password='toor', database='faceRegistration'):
        self.db = mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()
        self.table = table
        self.name = name
        self.photoPath = photoPath
    
    def createSQL(self):
        if self.table == 'pupils':
            sql = f"INSERT INTO {self.table} (name, photo) VALUES (%s, %s)"
        elif self.table == 'cameras':
            sql = f"INSERT INTO {self.table}(location) VALUES (%s,)"
        return sql

    def main(self):
        if self.table == 'pupils':
            val = (self.name, self.photoPath)
        elif self.table == 'cameras':
            val = self.name
        else:
            print(f'No tables called {self.table}')
            return
        sql = self.createSQL()
        self.cursor.execute(sql, val)
        self.db.commit()

Insert('cameras', 'Will_Laptop').main()