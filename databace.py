import pymysql as pm

class MiniBank:
    def __init__(self):
        self.db = pm.connect('localhost', 'root', 'root', 'hvpm')
        self.cursor = self.db.cursor()
    def die(self):
        self.db.close()
    def checklogin(self, log, pas):
       self.query = "select * from snuser where email = '%s' and password = '%s'" %(log, pas)
       self.cursor.execute(self.query)
       if self.cursor.rowcount :
          return True
       else:
           return False



    def storeLogin(self, email, pass1, uname, phoneno,dob,loc,gen):
        NU = 0
        self.sql = "insert into snuser values('%d','%s','%s','%s','%s','%s','%s','%s')" % (NU , uname, email, phoneno, pass1, dob, loc, gen)
        self.cursor.execute(self.sql)
        try:
            self.db.commit()
            self.status = True
            return self.status
            return
        except:
            self.db.rollback()
            self.status = False
            return self.status
        return



    def showdata(self):
        cursor = self.db.cursor()
        self.sql = "select * from users"

        try:
            self.cursor.execute(self.sql)
            result = cursor.fetchall()
            return result

        except:

            self.db.close()

    def updatepass(self, email, pass1):

        self.sql = "update snuser set password = '%s' where email = '%s'" % (pass1,email)

        self.cursor.execute(self.sql)
        try:
                self.db.commit()
                self.status = True
                return self.status
                return
        except:
                self.db.rollback()
                self.status = False
                return self.status
        return