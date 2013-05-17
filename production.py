class Production:
	def __init__(self, rule):
		rule = rule.strip('{ ,}\n').replace(',','')
		left, dummy, right = rule.partition(' > ')
		self.leftSide = left
		self.rightSide = right
	
	def useOn(self, string):
		helper = string.split(' ')
		try:
			replace = helper.index(self.leftSide)
		except ValueError:
			return string
		helper[replace] = self.rightSide
		string = " ".join(helper)
		return string
	def getLeftSide(self):
		return self.leftSide
	def getRightSide(self):
		return self.rightSide
		

p = Production("{ V > the }")
q = Production("{ VP > V NP }")
print p.useOn("V cat")
print q.useOn("NP VP")
