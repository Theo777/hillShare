import dataset
from HillshareMessage import Message

class MessageDao:
	def __init__(self, groupnames):
                self.groupname="_".join(groupnames.split())
		self.connectString= 'sqlite:///'+self.groupname+'Messages.db'
		self.db = dataset.connect(self.connectString)
		self.table = self.db[self.groupname+'Messages']
		
	def rowToMessage(self,row):
		message= Message(row['username'], row['mess'], row['profpic'])
		return message
	
	def messageToRow(self, message):
		row = dict(username=message.username, mess=message.mess, profpic=message.profpic )
                return row
                
	def selectByName(self,name):
		rows = self.table.find(username=username)
		result=[]
		
		if (rows is None):
			print('MessageDao: selectByID failed to find Message with ID '+ID+' and filename '+ filename)
			result= None
		else:
			count=0
			for row in rows:
					result.append(self.rowToMessage(row))
					count = count + 1
					
		return result
			
	def insertMessagetoGroup(self, mess):
		self.table.insert(self.messageToRow(mess))
		self.db.commit()
		
			
	def selectAll(self):
		table =self.db[self.groupname+'Messages']
		rows =table.all()
		
		result = []
		for row in rows:
			result.append(self.rowToMessage(row))
			
		return result
		
	def insert(self, mess):
		self.table.insert(self.messageToRow(mess))
		self.db.commit()
	
	def update(self, mess):
		self.table.update(self.messageToRow(mess),['username'])
		self.db.commit()
		
	def delete(self, message):
		self.table.delete(username=message.username)
		self.db.commit()
		
	def populate(self, user):
		self.table.insert(self.messageToRow(('Neil','test1')))
		self.table.insert(self.messageToRow(('Neil','test2')))
		self.table.insert(self.messageToRow(('Neil','test3')))
		self.table.insert(self.messageToRow(('Theo','test1')))
		self.table.insert(self.messageToRow(('Theo','test2')))
		self.db.commit()
