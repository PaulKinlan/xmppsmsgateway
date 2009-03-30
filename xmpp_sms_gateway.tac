from twisted.application import service
from twisted.words.protocols.jabber import component

import xmpp_sms_gateway
import simplejson

configuration = simplejson.load(file("daemon-conf.json", "r"))

application = service.Application(configuration["service"])

sm = component.buildServiceManager(configuration["server"], configuration["secret"],
                (configuration["port"]))

# Turn on verbose mode, this will be equivilant to the CDR
xmpp_sms_gateway.LogService().setServiceParent(sm)

# set up our example Service
s = xmpp_sms_gateway.XMPPSMSService()
s.setServiceParent(sm)

sm.setServiceParent(application)
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
"xmpp_sms_gateway.tac" 21 lines, 645 characters
