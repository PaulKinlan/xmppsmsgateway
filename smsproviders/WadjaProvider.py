import SMSProvider

import urllib

class WadjaProvider(SMSProvider.SMSProvider):
	def __init__(self, configuration):
		self.configuration = configuration
	
	def Send(self, sms):
		key = self.configuration["key"]
	
		
		url = 'http://sms.wadja.com/partners/sms/default.aspx'
		values = { 
					'key' : key,
					'msg' : sms.message,
					'to'  : sms.to,
					'form': sms.from_address,
					'send': 1,
					'unicode': 'no'
				}
			
		url_values = urllib.urlencode(values)
		data = urllib.urlopen(url + '?' + url_values)
		        
		return data.read()
		 
	