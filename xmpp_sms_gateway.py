
# Standard Libraries
import urllib2
import time
import re

# General Libraries
import simplejson

#Twisted Libraries
from twisted.words.protocols.jabber import jid, xmlstream
from twisted.application import internet, service
from twisted.internet import interfaces, defer, reactor
from twisted.python import log
from twisted.words.xish import domish
from twisted.words.protocols.jabber.ijabber import IService
from twisted.words.protocols.jabber import component
from zope.interface import Interface, implements

# SMS providers
import smsproviders

MESSAGE  = '/message'  # message xpath

def create_reply(elem):
	""" switch the 'to' and 'from' attributes to reply to this element """
	# NOTE - see domish.Element class to view more methods
	frm = elem['from']
	elem['from'] = elem['to']
	elem['to']   = frm

	return elem

class LogService(component.Service):
	"""
	A service to log incoming and outgoing xml to and from our XMPP component.
	"""

	def transportConnected(self, xmlstream):
		xmlstream.rawDataInFn = self.rawDataIn
		xmlstream.rawDataOutFn = self.rawDataOut

	def rawDataIn(self, buf):
		log.msg("%s - RECV: %s" % (str(time.time()), unicode(buf, 'utf-8').encode('ascii', 'replace')))

		log.msg("%s - SEND: %s" % (str(time.time()), unicode(buf, 'utf-8').encode('ascii', 'replace')))
	def rawDataOut(self, buf):
		pass

class SMS():
	"""
	An SMS that will be sent to the provider.
	"""
	
	def __init__(self, to, from_address, message):
		self.to = to
		self.from_address = from_address
		self.message = message

class XMPPSMSService(component.Service):
	"""
	XMPP SMS Gateway:
		recieves IM's and sends them to the mobile using configured providers
		You can send SMS's to any JID as long as it is in the following format dddddddddddddd@{servername}
	"""
	implements(IService)
	
	def __init__(self):
		self.configuration = simplejson.load(file("provider-conf.json", "r"))

	def componentConnected(self, xmlstream):
		"""
		This method is called when the componentConnected event gets called.
		That event gets called when we have connected and authenticated with the XMPP server.
		"""

		self.jabberId = xmlstream.authenticator.otherHost
		self.xmlstream = xmlstream # set the xmlstream so we can reuse it

		xmlstream.addObserver(MESSAGE, self.onMessage, 1)

	def onMessage(self, msg):
		"""
		Act on the message stanza that has just been received.
		Load the correct module and send a message to that.
		"""
		# return to sender
		msg = create_reply(msg)

		self.xmlstream.send(msg) # send the modified domish.Element
		to = re.sub("@.*", "", msg['from'])
		sms = SMS(to, '', msg.body)

		factory = smsproviders.ProviderFactory()
		provider = factory.Create(self.configuration)
		provider.Send(sms)

		log.msg("%s %s" % (msg.body, to))  
	
def main():	
	sms = SMS('447730517944', '', 'TEST MESSAGE')
	configuration = simplejson.load(file("provider-conf.json", "r"))
	factory = smsproviders.ProviderFactory()
	provider = factory.Create(configuration)
	provider.Send(sms)
	
if __name__ == '__main__':
	main()