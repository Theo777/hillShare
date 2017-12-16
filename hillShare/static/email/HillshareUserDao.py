import dataset
from HillshareUser import User

class UserDao:
	def __init__(self):
		self.connectString = 'sqlite:///users.db'
        self.db = dataset.connect(self.connectString)
        self.table = self.db['users']
        
        def rowToUser(self,row):
        user = User(row['userid'], row['password'], row['studentEmail'], row['profPic'], row['groups'])
        return user

    def userToRow(self,user):
        row = dict(userid=user.userid, password=user.password, studentEmail=user.studentEmail, profPic=user.profPic, groups=user.groups)
        return row

    def selectByUserid(self,userid):
        rows   = self.table.find(userid=userid)

        if (rows is None):
            print('UserDao:selectByUserid failed to find user with ' + userid)
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    print('UserDao:selectByUserid more than one user selected with ' + userid)
                    return None
                else:
                    result = self.rowToUser(row)
                    count = count + 1
                    
        return result
        
         def selectBystudentEmail(self,studentEmail):
        rows   = self.table.find(studentEmail=self.studentEmail)

        if (rows is None):
            print('UserDao:selectByUserid failed to find user with ' + userid)
            result = None
        else:
            count = 0
            for row in rows:
                if (count > 0):
                    print('UserDao:selectByUserid more than one user selected with ' + userid)
                    return None
                else:
                    result = self.rowToUser(row)
                    count = count + 1
                    
		return result

    def selectAll(self):
        table = self.db['users']
        rows   = table.all()

        result = []
        for row in rows:
            result.append(self.rowToUser(row))

        return result
        
    def insert(self,user):
        self.table.insert(self.userToRow(user))
        self.db.commit()

    def update(self,user):
        self.table.update(self.userToRow(user),['userid'])
        self.db.commit()

    def delete(self,user):
        self.table.delete(userid=user.userid)
        self.db.commit()

    def populate(self):
        self.table.insert(self.userToRow(User('Neil','csrocks55','Neil@stonehill','',[])))
        self.table.insert(self.userToRow(User('Theo','csrocks55','Theo@stonehill','asshole.jpg',[])))
        self.table.insert(self.userToRow(User('Will','csrocks55','Will@stonehill','',[])))
        self.db.commit()
