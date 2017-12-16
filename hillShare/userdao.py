import dataset
from user import User
import logging
from flask import current_app

class UserDao:
        
        def __init__(self):
	        self.connectString = 'sqlite:///users.db'
                self.db = dataset.connect(self.connectString)
                self.table = self.db['users']
                try:
                        self.logger = current_app.logger
                except:
                        self.logger = logging.getLogger('root')

                self.logger.debug('got to UserDao')
        
                
        def rowToUser(self,row):
                user = User(row['userid'], row['password'], row['studentEmail'], row['profPic'], row['member'])
                return user

        def userToRow(self,user):
            
            row = dict(userid=user.userid, password=user.password, studentEmail=user.studentEmail, profPic=user.profPic, member=user.member)
            return row

        def returnUserList(self,userid):
                rows =self.table.find(userid=userid)
                result=None

                if (rows is None):
                        result = None
                else:
                        count=0
                        for row in rows:
                                if (count > 0):
                                        return None
                                else:
                                        result= self.rowToUser(row)
                                        count=count + 1

                memberString=result.member

                memberList=memberString.split("\n")

                return memberList

        def selectByUserid(self,userid):
                
                rows   = self.table.find(userid=userid)
                result =None
                
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
                rows   = self.table.find(studentEmail=studentEmail)
                
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
                
        def updateMember(self,user):
                self.table.update(self.userToRow(user),['userid'])
                self.db.commit()

        def addMember(self, username, newUser):
                user=self.selectByUserid(username)
                if(not user.member):
                        user.member=newUser
                        
                else:
                        user.member=user.member+'\n'+newUser
                self.updateMember(user)
            
        def delete(self,user):
                self.table.delete(userid=user.userid)
                self.db.commit()

        def populate(self):
                self.table.insert(self.userToRow(User('Neil','csrocks55','Neil@stonehill','default')))
                self.table.insert(self.userToRow(User('Theo','csrocks55','Theo@stonehill','default')))
                self.table.insert(self.userToRow(User('Will','csrocks55','Will@stonehill','default')))
                self.db.commit()
        
