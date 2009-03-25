from CDRProvider import CDRProvider

import urllib

class FlatFileProvider(CDRProvider.CDRProvider):
	def __init__(self, configuration):
		self.configuration = configuration
	
	def Log(self, sms):
		
		 
	