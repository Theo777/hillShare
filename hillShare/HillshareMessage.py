class Message:
	def __init__(self, username, mess, profpic):
		self.username=username
		self.mess=mess
                self.profpic=profpic
                
	def toString(self):
		return self.username+" "+self.mess+" "+self.profpic

        def JJ(self):
                temp=[self.username,self.mess,self.profpic]
                
                return temp
