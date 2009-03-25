def logging(fn):
	def log(*args):
		print "Logged"
		return fn(*args)
	return log

class SMSProvider():
	@logging
	def Send(self, sms):
		pass

