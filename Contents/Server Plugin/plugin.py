#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Chad Francis. All rights reserved.
# http://www.chadfrancis.com

import httplib, urllib, sys, os

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

	def setVolume(self, pluginAction):
		# set volume, confirm and update local var
		self.debugLog(u"setVolume called")

	def getStatus(self, pluginAction):
		# get status from receiver, update locals
		self.debugLog(u"getStatus called")

	def setPower(self, pluginAction):
		# set power, confirm and update local var
		self.debugLog(u"setPower called")

	def setSleep(self, pluginAction):
		# set sleep, confirm and update local var
		self.debugLog(u"setSleep called")

	def setInput(self, pluginAction):
		# change input, confirm and update local var
		self.debugLog(u"setInput called")

