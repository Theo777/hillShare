class User:
	def __init__(self, userid, password, studentEmail, profPic, member):
		self.userid=userid
		self.password=password
		self.studentEmail=studentEmail
		self.profPic=profPic
                self.member=member
		
		
	def toString(self):
		return self.userid+" "+self.password+" "+self.studentEmail+" " +self.profPic+self.member
		
