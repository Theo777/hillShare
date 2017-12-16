class Event:
	def __init__(self, day, month, year, endDay, endMonth, endYear, startTime, endTime, name, description, group, tags):
		self.day=day
		self.month=month
		self.year=year
		self.endDay=endDay
		self.endMonth=endMonth
		self.endYear=endYear
		self.startTime=startTime
		self.endTime = endTime
		self.name = name
		self.description=description
		self.group = group
		self.tags=tags
		
	def toString(self):
		return self.day+" "+self.month+" "+self.year+" "+self.time+" " +  + " "+self.name+" "+self.description+" "+self.tags
		
