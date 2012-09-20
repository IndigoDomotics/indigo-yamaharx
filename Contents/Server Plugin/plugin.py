#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Chad Francis. All rights reserved.
# http://www.chadfrancis.com

import httplib, urllib2, sys, os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def str2bool(v):
	return v.lower() in ("yes", "true", "t", "1")

def xmitToReceiver(receiverIp, xml_string):
	url = 'http://'+receiverIp+'/YamahaRemoteControl/ctrl'

	req = urllib2.Request(
		url=url, 
		data=xml_string, 
		headers={'Content-Type': 'application/xml'})
	resp = urllib2.urlopen(req)
	status_xml = resp.read()
	root = ET.fromstring(status_xml)
	return root

class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)


	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	# actions go here
	def turnOn(self, pluginAction):
		# set power to on, confirm and update local var
		self.debugLog(u"turnOn called")

	def turnOff(self, pluginAction):
		# set power to off, confirm and update local var
		self.debugLog(u"turnOff called")

	def sleep(self, pluginAction):
		# set sleep to on, confirm and update local var
		self.debugLog(u"sleep called")

	def wake(self, pluginAction):
		# set sleep to off, confirm and update local var
		self.debugLog(u"wake called")

	def toggleMute(self, pluginAction, dev):
		# set sleep to off, confirm and update local var
		self.debugLog(u"toggleMute called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		new_mute_state = 'On' if dev.states['mute']=='Off' else 'Off'
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Mute>'+new_mute_state+'</Mute></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def setVolume(self, pluginAction, dev):
		# set volume, confirm and update local var
		self.debugLog(u"setVolume called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		new_level = pluginAction.props['txtvolume']
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+new_level+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def getStatus(self, pluginAction, dev):
		# get status from receiver, update locals
		self.debugLog(u"getStatus called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		xml_string = '<YAMAHA_AV cmd="GET"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		power = root.find("./Main_Zone/Basic_Status/Power_Control/Power").text
		sleep = root.find("./Main_Zone/Basic_Status/Power_Control/Sleep").text
		volume = root.find("./Main_Zone/Basic_Status/Vol/Lvl/Val").text
		mute = root.find("./Main_Zone/Basic_Status/Vol/Mute").text
		inputmode = root.find("./Main_Zone/Basic_Status/Input/Input_Sel").text

		dev.updateStateOnServer("power", power)
		dev.updateStateOnServer("sleep", sleep)
		dev.updateStateOnServer("volume", volume)
		dev.updateStateOnServer("mute", mute)
		dev.updateStateOnServer("input", inputmode)

	def setPower(self, pluginAction):
		# set power, confirm and update local var
		self.debugLog(u"setPower called")

	def setSleep(self, pluginAction):
		# set sleep, confirm and update local var
		self.debugLog(u"setSleep called")

	def setInput(self, pluginAction):
		# change input, confirm and update local var
		self.debugLog(u"setInput called")

