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
	
	def setMute(self, pluginAction, dev, newStateVal):
		# set value of mute
		self.debugLog(u"setMute called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		if newStateVal is None:
			#need to pick up new mute state from action config
			newStateVal = 'Off';

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Mute>'+newStateVal+'</Mute></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def toggleMute(self, pluginAction, dev):
		# toggle mute value, confirm and update local var
		self.debugLog(u"toggleMute called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = 'On' if dev.states['mute']=='Off' else 'Off'
		self.setMute(pluginAction, dev, newStateVal)

	def setVolume(self, pluginAction, dev):
		# set volume, confirm and update local var
		self.debugLog(u"setVolume called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = pluginAction.props['txtvolume']
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+newStateVal+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def setPower(self, pluginAction, dev, newStateVal):
		# set value of power
		self.debugLog(u"setPower called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		if newStateVal is None:
			#need to pick up new power state from action config
			newStateVal = 'On';

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+newStateVal+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
		self.debugLog(xml_string)
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def togglePower(self, pluginAction, dev):
		# toggle power value, confirm and update local var
		self.debugLog(u"togglePower called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = 'On' if (dev.states['power']=='Standby' or dev.states['power']=='Off') else 'Standby'
		self.setPower(pluginAction, dev, newStateVal)

	def setSleep(self, pluginAction, dev, newStateVal):
		# set value of sleep
		self.debugLog(u"setSleep called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		if newStateVal is None:
			#need to pick up new sleep state from action config
			newStateVal = 'On';

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>'+newStateVal+'</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

	def toggleSleep(self, pluginAction, dev):
		# toggle sleep value, confirm and update local var
		self.debugLog(u"toggleSleep called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = 'On' if dev.states['sleep']=='Off' else 'Off'
		self.setSleep(pluginAction, dev, newStateVal)

	def setInput(self, pluginAction):
		# change input, confirm and update local var
		self.debugLog(u"setInput called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = pluginAction.props['newinput']

		if newStateVal is None:
			self.debugLog(u"no input selected")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Basic_Status><Input><Input_Sel>'+newStateVal+'</Input></Input_Sel></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.getStatus(pluginAction, dev)

