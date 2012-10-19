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

	def deviceStartComm(self, dev):
		self.updateStatus(dev)

	def updateStatus(self, dev):
		# get status from receiver, update locals
		self.debugLog(u"updating status...")

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


	# actions go here
	def getStatus(self, pluginAction, dev):
		self.updateStatus(dev)
	
	def setMute(self, pluginAction, dev, newStateVal=None):
		# set value of mute
		self.debugLog(u"setMute called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		if newStateVal is None:
			newStateVal = pluginAction.props['ddlmute']

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Mute>'+newStateVal+'</Mute></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

	def toggleMute(self, pluginAction, dev):
		# toggle mute value, confirm and update local var
		self.debugLog(u"toggleMute called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.updateStatus(dev)
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
		self.updateStatus(dev)

	def increaseVolume(self, pluginAction, dev):
		# increase volume, confirm and update local var
		self.debugLog(u"increaseVolume called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.updateStatus(dev)
		incrementVal = int(pluginAction.props['txtincrement'])
		currentVol = int(dev.states['volume'])
		newStateVal = currentVol+incrementVal
		self.debugLog(str(newStateVal))
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+str(newStateVal)+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

	def decreaseVolume(self, pluginAction, dev):
		# decrease volume, confirm and update local var
		self.debugLog(u"decreaseVolume called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.updateStatus(dev)
		incrementVal = int(pluginAction.props['txtincrement'])
		currentVol = int(dev.states['volume'])
		newStateVal = currentVol-incrementVal
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+str(newStateVal)+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

	def setPower(self, pluginAction, dev, newStateVal):
		# set value of power
		self.debugLog(u"setPower called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		if newStateVal is None:
			newStateVal = pluginAction.props['ddlpower']

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+newStateVal+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

	def togglePower(self, pluginAction, dev):
		# toggle power value, confirm and update local var
		self.debugLog(u"togglePower called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.updateStatus
		newStateVal = 'On' if (dev.states['power']=='Standby' or dev.states['power']=='Off') else 'Standby'
		self.setPower(pluginAction, dev, newStateVal)

	def setSleep(self, pluginAction, dev):
		# set value of sleep
		self.debugLog(u"setSleep called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = pluginAction.props['ddlsleep'].replace('n','')
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>'+newStateVal+'</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

	def setInput(self, pluginAction):
		# change input, confirm and update local var
		self.debugLog(u"setInput called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		newStateVal = pluginAction.props['newinput'].upper().replace(".","/").replace("_"," ")

		if newStateVal is None:
			self.debugLog(u"no input selected")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Basic_Status><Input><Input_Sel>'+newStateVal+'</Input></Input_Sel></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev.pluginProps['txtip'], xml_string)
		self.updateStatus(dev)

