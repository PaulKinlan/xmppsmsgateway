from twisted.application import service
from twisted.words.protocols.jabber import component

import xmpp_sms_gateway
import simplejson

configuration = simplejson.load("daemon-conf.json")

application = service.Application(configuration.service)

sm = component.buildServiceManager(configration.server, configuration.secret,
                (configuration.port))

# Turn on verbose mode, this will be equivilant to the CDR
xmpp_sms.LogService().setServiceParent(sm)

# set up our example Service
s = xmpp_sms.XMPPSMSService()
s.setServiceParent(sm)

sm.setServiceParent(application)
