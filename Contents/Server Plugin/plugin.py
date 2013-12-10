#! /usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib2, sys, os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def str2bool(v):
	return v.lower() in ("yes", "true", "t", "1")

def xmitToReceiver(dev, xml_string):
	url = 'http://'+dev.pluginProps['address']+'/YamahaRemoteControl/ctrl'

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

	def runConcurrentThread(self):
		self.debugLog(u"started polling")
		try:
			while True:
				# update the status on each instance every 10 seconds
				self.sleep(10)
				for dev in indigo.devices.iter("self"):
					# call the update method with the device instance
					self.updateStatus(dev)
		except self.StopThread:
			pass

	# helper methods, these mostly serve to facilitate calls to the device

	def updateStatus(self, dev):
		# get status from receiver, update locals
		self.debugLog(u"updating status...")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		xml_string = '<YAMAHA_AV cmd="GET"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		power = root.find("./Main_Zone/Basic_Status/Power_Control/Power").text
		sleep = root.find("./Main_Zone/Basic_Status/Power_Control/Sleep").text
		if(sleep!='Off'): sleep = "n"+sleep
		volume = root.find("./Main_Zone/Basic_Status/Vol/Lvl/Val").text
		mute = root.find("./Main_Zone/Basic_Status/Vol/Mute").text
		inputmode = root.find("./Main_Zone/Basic_Status/Input/Input_Sel").text

		dev.updateStateOnServer("power", value=power)
		dev.updateStateOnServer("sleep", value=sleep)
		dev.updateStateOnServer("volume", value=volume)
		self.debugLog(u"mute value is: "+mute)
		dev.updateStateOnServer("mute", value=mute, uiValue="farts")
		dev.updateStateOnServer("input", value=inputmode)

	def putMute(self, dev, val):
		if dev is None:
			self.debugLog(u"no device defined")
			return

		if val is None:
			self.debugLog(u"value not defined")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Mute>'+val+'</Mute></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putVolume(self, dev, val):
		if dev is None:
			self.debugLog(u"no device defined")
			return

		if val is None:
			self.debugLog(u"value not defined")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putPower(self, dev, val):
		if dev is None:
			self.debugLog(u"no device defined")
			return

		if val is None:
			self.debugLog(u"value not defined")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+val+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putSleep(self, dev, val):
		if dev is None:
			self.debugLog(u"no device defined")
			return

		if val is None:
			self.debugLog(u"value not defined")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>'+val+'</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putInput(self, dev, val):
		if dev is None:
			self.debugLog(u"no device defined")
			return

		if val is None:
			self.debugLog(u"value not defined")
			return

		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Basic_Status><Input><Input_Sel>'+val+'</Input></Input_Sel></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)


	# actions go here
	def getStatus(self, pluginAction, dev):
		self.updateStatus(dev)
		self.getDeviceDisplayStateId(dev)
	
	def setMute(self, pluginAction, dev):
		self.debugLog(u"setMute called")
		val = pluginAction.props['ddlmute']
		self.putMute(dev, val)

	def toggleMute(self, pluginAction, dev):
		self.debugLog(u"toggleMute called")
		self.updateStatus(dev)
		val = 'On' if dev.states['mute']=='Off' else 'Off'
		self.putMute(dev, val)

	def setVolume(self, pluginAction, dev):
		self.debugLog(u"setVolume called")
		val = pluginAction.props['txtvolume']
		self.putVolume(dev, val)

	def increaseVolume(self, pluginAction, dev):
		self.debugLog(u"increaseVolume called")
		self.updateStatus(dev)
		val = str(int(dev.states['volume']) + int(pluginAction.props['txtincrement']))
		self.putVolume(dev, val)

	def decreaseVolume(self, pluginAction, dev):
		self.debugLog(u"decreaseVolume called")
		self.updateStatus(dev)
		val = str(int(dev.states['volume']) - int(pluginAction.props['txtincrement']))
		self.putVolume(dev, val)

	def setPower(self, pluginAction, dev):
		self.debugLog(u"setPower called")
		val = pluginAction.props['ddlpower']
		self.putPower(dev, val)

	def togglePower(self, pluginAction, dev):
		self.debugLog(u"togglePower called")
		self.updateStatus(dev)
		val = 'On' if (dev.states['power']=='Standby') else 'Standby'
		self.putPower(dev, val)

	def setSleep(self, pluginAction, dev):
		self.debugLog(u"setSleep called")
		val = pluginAction.props['ddlsleep'].replace('n','')
		self.putSleep(dev, val)

	def setInput(self, pluginAction, dev):
		self.debugLog(u"setInput called")
		val = pluginAction.props['newinput'].upper().replace(".","/").replace("_"," ")
		self.putInput(dev, val)

