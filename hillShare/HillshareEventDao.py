import dataset
import time
import datetime
from HillshareEvent import Event
from operator import attrgetter
import sys

class EventDao:
	def __init__(self, ):
		self.connectString= 'sqlite:///Event.db'
		self.db = dataset.connect(self.connectString)
		self.table = self.db['Event']
		
	def rowToEvent(self,row):
		event = Event(row['day'], row['month'], row['year'], row['endDay'], row['endMonth'], row['endYear'], row['startTime'], row['endTime'], row['name'], row['description'], row['group'], row['tags'])
		return event
	
	def eventToRow(self, event):
		row = dict(day=event.day, month=event.month, year=event.year, endDay=event.endDay, endMonth=event.endMonth, endYear=event.endYear, startTime=event.startTime, endTime=event.endTime, name=event.name, description=event.description, group=event.group, tags=event.tags)
		return row
		
	def selectByName(self,name):
		rows = self.table.find(name=name)
		result=[]
		
		if (rows is None):
			print('MessageDao: selectByID failed to find Message with ID '+ID+' and filename '+ filename)
			result= None
		else:
			count=0
			for row in rows:
					result.append(self.rowToEvent(row))
					count = count + 1
					
		return result
			
	def insertEvent(self, event):
		self.table.insert(self.eventToRow(event))
		self.db.commit()
		
			
	def selectAll(self):
		table =self.db['Event']
		rows =table.all()
		
		result = []
		for row in rows:
			result.append(self.rowToEvent(row))
			
		return sorted(result ,key= attrgetter('year','month','day','startTime'))
		
	def sort(self):
		sorted(self.table, key="name")
		self.db.commit()
		
	
	def expire(self):
		events = self.selectAll()
		currentDate = time.strftime("%x")
		currentTime = time.strftime("%X")
                print >> sys.stderr, currentDate
		raw  = currentDate.split("/")
                print >> sys.stderr, raw
                raw2 = currentTime.split(":")
                if((int(raw2[0])-4) < 0):
                        raw2[0]=str((int(raw2[0])-4)+24)
                        raw[1]=str((int(raw[1])-1))
                currentTime=str(raw2[0])+str(raw2[1])
                raw[2]='20'+raw[2]
                print >> sys.stderr, raw
		eventsToday = []               
		for Event in events:
			if(Event.endDay==raw[1] and Event.endMonth==raw[0] and Event.endYear==raw[2]):
                                print >> sys.stderr, Event.name +' was added to eventsday'
			        eventsToday.append(Event)
				
		for Event in eventsToday:
                        temp = Event.endTime.replace(":","")
                        print >> sys.stderr, 'currentTime: '+currentTime
                        print >> sys.stderr, 'temp: '+temp
			if(int(currentTime) > int(temp)):
                                print >> sys.stderr, 'currentime > temp'
                                self.table.delete(name=Event.name)
				
		self.db.commit()
				
	def insert(self, event):
		self.table.insert(self.eventToRow(event))
		self.db.commit()
	
	def update(self, event):
		self.table.update(self.eventToRow(event),['username'])
		self.db.commit()
		
	def delete(self, event):
		self.table.delete(name=event.name)
		self.db.commit()
		
	def populate(self):
		self.db.commit()
