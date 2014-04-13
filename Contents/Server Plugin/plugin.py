#! /usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib2, sys, os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def str2bool(v):
	return v.lower() in ('yes', 'true', 't', '1')

def xmitToReceiver(dev, xml_string):
	url = 'http://'+dev.pluginProps['txtip']+'/YamahaRemoteControl/ctrl'
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
		self.deviceList = []
		self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)


	def startup(self):
		self.debugLog(u'startup called')

	def shutdown(self):
		self.debugLog(u'shutdown called')

	def deviceStartComm(self, dev):
		self.updateStatus(dev)

	# helper methods, these mostly serve to facilitate calls to the device
	def updateStatus(self, dev):
		# get status from receiver, update locals
		# self.debugLog(u'updating status...')
		if dev is None:
			self.debugLog(u'no device defined')
			return
		xml_string = '<YAMAHA_AV cmd="GET"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		power = root.find('./Main_Zone/Basic_Status/Power_Control/Power').text
		sleep = root.find('./Main_Zone/Basic_Status/Power_Control/Sleep').text
		dsleep = sleep
		if(sleep!='Off'): sleep = 'n'+sleep.replace(' min','')
		volume = root.find('./Main_Zone/Basic_Status/Volume/Lvl/Val').text
		dvolume = (str(float(volume) / 10)+' dB').replace('.', ',')
		mute = root.find('./Main_Zone/Basic_Status/Volume/Mute').text
		swtrim = root.find('./Main_Zone/Basic_Status/Volume/Subwoofer_Trim/Val').text
		dswtrim = (str(float(swtrim) / 10)+' dB').replace('.', ',')
		input = root.find('./Main_Zone/Basic_Status/Input/Input_Sel').text
		if (input == 'SERVER' or input == 'NET RADIO' or input == 'USB' or input == 'AirPlay'):
			if (input == 'NET RADIO'):
				source = input.replace(' ', '_')
			else:
				source = input
			xml_string = '<YAMAHA_AV cmd="GET"><'+source+'><Play_Info>GetParam</Play_Info></'+source+'></YAMAHA_AV>'
			playinfo = xmitToReceiver(dev, xml_string)
			if (playinfo.find('./'+source+'/Play_Info/Feature_Availability').text == 'Ready'):
				playback = playinfo.find('./'+source+'/Play_Info/Playback_Info').text
				if (source == 'NET_RADIO'):
					repeat = 'Off'
					shuffle = 'Off'
					artist = playinfo.find('./'+source+'/Play_Info/Meta_Info/Station').text
				else:
					repeat = playinfo.find('./'+source+'/Play_Info/Play_Mode/Repeat').text
					shuffle = playinfo.find('./'+source+'/Play_Info/Play_Mode/Shuffle').text
					artist = playinfo.find('./'+source+'/Play_Info/Meta_Info/Artist').text
				album = playinfo.find('./'+source+'/Play_Info/Meta_Info/Album').text
				song = playinfo.find('./'+source+'/Play_Info/Meta_Info/Song').text
#				song = playinfo.find('./'+source+'/Play_Info/Meta_Info/Song').text.replace('&amp;', '&')
			else:
				playback = 'Off'
				repeat = 'Off'
				shuffle = 'Off'
				artist = ''
				album = ''
				song = ''
			if (source == 'SERVER' or source == 'NET_RADIO' or source == 'USB'):
				xml_string = '<YAMAHA_AV cmd="GET"><'+source+'><List_Info>GetParam</List_Info></'+source+'></YAMAHA_AV>'
				listinfo = xmitToReceiver(dev, xml_string)
				if (listinfo.find('./'+source+'/List_Info/Menu_Status').text == 'Ready'):
					listname = listinfo.find('./'+source+'/List_Info/Menu_Name').text
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_1/Attribute').text != 'Unselectable'):
						line1 = listinfo.find('./'+source+'/List_Info/Current_List/Line_1/Txt').text
					else: line1 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_2/Attribute').text != 'Unselectable'):
						line2 = listinfo.find('./'+source+'/List_Info/Current_List/Line_2/Txt').text
					else: line2 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_3/Attribute').text != 'Unselectable'):
						line3 = listinfo.find('./'+source+'/List_Info/Current_List/Line_3/Txt').text
					else: line3 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_4/Attribute').text != 'Unselectable'):
						line4 = listinfo.find('./'+source+'/List_Info/Current_List/Line_4/Txt').text
					else: line4 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_5/Attribute').text != 'Unselectable'):
						line5 = listinfo.find('./'+source+'/List_Info/Current_List/Line_5/Txt').text
					else: line5 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_6/Attribute').text != 'Unselectable'):
						line6 = listinfo.find('./'+source+'/List_Info/Current_List/Line_6/Txt').text
					else: line6 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_7/Attribute').text != 'Unselectable'):
						line7 = listinfo.find('./'+source+'/List_Info/Current_List/Line_7/Txt').text
					else: line7 = ''
					if (listinfo.find('./'+source+'/List_Info/Current_List/Line_8/Attribute').text != 'Unselectable'):
						line8 = listinfo.find('./'+source+'/List_Info/Current_List/Line_8/Txt').text
					else: line8 = ''
					linesel = listinfo.find('./'+source+'/List_Info/Cursor_Position/Current_Line').text
					page = (float(linesel)/8)
					if (page <= int(page)):
						page = int(page)-1
					else: page = int(page)
					linesel = int(linesel)-page*8
					linesel = 's'+str(linesel)
				else:
					listname = ''
					line1 = ''
					line2 = ''
					line3 = ''
					line4 = ''
					line5 = ''
					line6 = ''
					line7 = ''
					line8 = ''
					linesel = 'na'
					page = ''
			band = 'Off'
			stereo = 'Off'
		elif (input == 'TUNER'):
			source = 'Tuner'
			playback = 'Off'
			repeat = 'Off'
			shuffle = 'Off'
			xml_string = '<YAMAHA_AV cmd="GET"><'+source+'><Play_Info>GetParam</Play_Info></'+source+'></YAMAHA_AV>'
			playinfo = xmitToReceiver(dev, xml_string)
			if (playinfo.find('./'+source+'/Play_Info/Feature_Availability').text == 'Ready'):
				band = playinfo.find('./'+source+'/Play_Info/Tuning/Band').text
				fqc = playinfo.find('./'+source+'/Play_Info/Tuning/Freq/Current/Val').text
				if (band == 'FM' and fqc.isdigit()):
					freq = str(float(fqc) / 100).replace('.', ',')
					unit = playinfo.find('./'+source+'/Play_Info/Tuning/Freq/Current/Unit').text
				else:
					freq = fqc
					unit = ''
				if (playinfo.find('./'+source+'/Play_Info/Signal_Info/Tuned').text == 'Assert'):
					if (playinfo.find('./'+source+'/Play_Info/Signal_Info/Stereo').text == 'Assert'):
						stereo = 'Auto'
					elif (playinfo.find('./'+source+'/Play_Info/Signal_Info/Stereo').text == 'Negate'):
						stereo = 'Mono'
					else: stereo = 'Off'
				else: stereo = 'Off'
				listname = str(band)+' '+str(freq)+' '+str(unit)
				stat = playinfo.find('./'+source+'/Play_Info/Meta_Info/Program_Service').text
				if (stat):
					statn = ' '.join(stat.split())
				else: statn = ''
				type = playinfo.find('./'+source+'/Play_Info/Meta_Info/Program_Type').text
				if (type):
					typ = ' - '+' '.join(type.split())
				else: typ = ''
				artist = statn+typ
				rt1 = playinfo.find('./'+source+'/Play_Info/Meta_Info/Radio_Text_A').text
				rt2 = playinfo.find('./'+source+'/Play_Info/Meta_Info/Radio_Text_B').text
				if (rt1):
					album = ' '.join(rt1.split()).replace('&amp;', '&')
				else: album = ''
				if (rt2):
					song = ' '.join(rt2.split()).replace('&amp;', '&')
				else: song = ''
			line1 = ''
			line2 = ''
			line3 = ''
			line4 = ''
			line5 = ''
			line6 = ''
			line7 = ''
			line8 = ''
			linesel = 'na'
			page = ''
		else:
			playback = 'Off'
			repeat = 'Off'
			shuffle = 'Off'
			artist = ''
			album = ''
			song = ''
			listname = ''
			line1 = ''
			line2 = ''
			line3 = ''
			line4 = ''
			line5 = ''
			line6 = ''
			line7 = ''
			line8 = ''
			linesel = 'na'
			page = ''
			band = 'Off'
			stereo = 'Off'
		inputmode = input.lower().replace(' ','_')
		inputname = root.find('./Main_Zone/Basic_Status/Input/Input_Sel_Item_Info/Title').text
		if (input.find('HDMI') != -1):
			dinput = inputname+' - '+input
		elif (input.find('AV') != -1):
			dinput = inputname+' - '+input
		elif (input.find('AUDIO') != -1):
			dinput = inputname+' - '+input
		else:
			dinput = inputname
		dspstraight = root.find('./Main_Zone/Basic_Status/Surround/Program_Sel/Current/Straight').text
		dspenh = root.find('./Main_Zone/Basic_Status/Surround/Program_Sel/Current/Enhancer').text
		dspprog = root.find('./Main_Zone/Basic_Status/Surround/Program_Sel/Current/Sound_Program').text
		if (dspstraight == 'Off'):
			ddsp = dspprog
		else:
			ddsp = 'Straight'
			dspprog = 'dspoff'
		if(dspprog == '2ch Stereo'):
			dspprog = dspprog.replace('2ch Stereo','twoch_Stereo')
		elif(dspprog == '7ch Stereo'):
			dspprog = dspprog.replace('7ch Stereo','sevench_Stereo')
		else:
			dspprog = dspprog.replace(' ','_')
		dsp3dcinema = root.find('./Main_Zone/Basic_Status/Surround/_3D_Cinema_DSP').text
		bass = root.find('./Main_Zone/Basic_Status/Sound_Video/Tone/Bass/Val').text
		dbass = (str(float(bass) / 10)+' dB').replace('.', ',')
		trebble = root.find('./Main_Zone/Basic_Status/Sound_Video/Tone/Treble/Val').text
		dtrebble = (str(float(trebble) / 10)+' dB').replace('.', ',')
		puredirect = root.find('./Main_Zone/Basic_Status/Sound_Video/Pure_Direct/Mode').text
		hdmiout1 = root.find('./Main_Zone/Basic_Status/Sound_Video/HDMI/Output/OUT_1').text
		hdmiout2 = root.find('./Main_Zone/Basic_Status/Sound_Video/HDMI/Output/OUT_2').text
		adaptivedrc = root.find('./Main_Zone/Basic_Status/Sound_Video/Adaptive_DRC').text
		dialoguelift = root.find('./Main_Zone/Basic_Status/Sound_Video/Dialogue_Adjust/Dialogue_Lift').text
		dialoguelvl = root.find('./Main_Zone/Basic_Status/Sound_Video/Dialogue_Adjust/Dialogue_Lvl').text
		if (power != 'Standby'):
			dev.updateStateOnServer('mute', mute)
			dev.updateStateOnServer('input', inputmode)
			dev.updateStateOnServer('dspstraight', dspstraight)
			dev.updateStateOnServer('dspenh', dspenh)
			dev.updateStateOnServer('dspprog', dspprog)
			dev.updateStateOnServer('dsp3dcinema', dsp3dcinema)
			dev.updateStateOnServer('puredirect', puredirect)
			dev.updateStateOnServer('hdmiout1', hdmiout1)
			dev.updateStateOnServer('hdmiout2', hdmiout2)
			dev.updateStateOnServer('adaptivedrc', adaptivedrc)
			dev.updateStateOnServer('band', band)
			dev.updateStateOnServer('stereo', stereo)
		else:
			dev.updateStateOnServer('mute', 'Off')
			dev.updateStateOnServer('input', 'inputoff')
			dev.updateStateOnServer('dspstraight', 'Off')
			dev.updateStateOnServer('dspenh', 'Off')
			dev.updateStateOnServer('dspprog', 'dspoff')
			dev.updateStateOnServer('dsp3dcinema', 'Off')
			dev.updateStateOnServer('puredirect', 'Off')
			dev.updateStateOnServer('hdmiout1', 'Off')
			dev.updateStateOnServer('hdmiout2', 'Off')
			dev.updateStateOnServer('adaptivedrc', 'Off')
			dev.updateStateOnServer('band', 'Off')
			dev.updateStateOnServer('stereo', 'Off')
		dev.updateStateOnServer('power', power)
		dev.updateStateOnServer('sleep', sleep)
		dev.updateStateOnServer('dsleep', dsleep)
		dev.updateStateOnServer('volume', volume)
		dev.updateStateOnServer('dvolume', dvolume)
		dev.updateStateOnServer('swtrim', swtrim)
		dev.updateStateOnServer('dswtrim', dswtrim)
		dev.updateStateOnServer('dinput', dinput)
		dev.updateStateOnServer('ddsp', ddsp)
		dev.updateStateOnServer('bass', bass)
		dev.updateStateOnServer('dbass', dbass)
		dev.updateStateOnServer('trebble', trebble)
		dev.updateStateOnServer('dtrebble', dtrebble)
		dev.updateStateOnServer('dialoguelift', dialoguelift)
		dev.updateStateOnServer('dialoguelvl', dialoguelvl)
		dev.updateStateOnServer('playback', playback)
		dev.updateStateOnServer('repeat', repeat)
		dev.updateStateOnServer('shuffle', shuffle)
		dev.updateStateOnServer('artist', artist)
		dev.updateStateOnServer('album', album)
		dev.updateStateOnServer('song', song)
		dev.updateStateOnServer('listname', listname)
		dev.updateStateOnServer('line1', line1)
		dev.updateStateOnServer('line2', line2)
		dev.updateStateOnServer('line3', line3)
		dev.updateStateOnServer('line4', line4)
		dev.updateStateOnServer('line5', line5)
		dev.updateStateOnServer('line6', line6)
		dev.updateStateOnServer('line7', line7)
		dev.updateStateOnServer('line8', line8)
		dev.updateStateOnServer('linesel', linesel)
		dev.updateStateOnServer('page', page)

	def putMute(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>'+val+'</Mute></Volume></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putVolume(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putSwtrim(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Subwoofer_Trim><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Subwoofer_Trim></Volume></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putPower(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+val+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putSleep(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>'+val+'</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putInput(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>'+val+'</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putScene(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Scene><Scene_Load>Scene '+val+'</Scene_Load></Scene></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putEnhancer(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Surround><Program_Sel><Current><Enhancer>'+val+'</Enhancer></Current></Program_Sel></Surround></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putStraight(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Surround><Program_Sel><Current><Straight>'+val+'</Straight></Current></Program_Sel></Surround></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putDSPProg(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Surround><Program_Sel><Current><Sound_Program>'+val+'</Sound_Program></Current></Program_Sel></Surround></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def put3dcinema(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Surround><_3D_Cinema_DSP>'+val+'</_3D_Cinema_DSP></Surround></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putBass(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Tone><Bass><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Bass></Tone></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putTrebble(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Tone><Treble><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Treble></Tone></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putPuredirect(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Pure_Direct><Mode>'+val+'</Mode></Pure_Direct></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putHdmiout1(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><System><Sound_Video><HDMI><Output><OUT_1>'+val+'</OUT_1></Output></HDMI></Sound_Video></System></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putHdmiout2(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><System><Sound_Video><HDMI><Output><OUT_2>'+val+'</OUT_2></Output></HDMI></Sound_Video></System></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putDlglift(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Dialogue_Adjust><Dialogue_Lift>'+val+'</Dialogue_Lift></Dialogue_Adjust></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putDlglvl(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Dialogue_Adjust><Dialogue_Lvl>'+val+'</Dialogue_Lvl></Dialogue_Adjust></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putAdaptivedrc(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Sound_Video><Adaptive_DRC>'+val+'</Adaptive_DRC></Sound_Video></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putMenu(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Cursor_Control><Menu_Control>'+val+'</Menu_Control></Cursor_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putCursor(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'SERVER' or source == 'NET_RADIO' or source == 'USB' or source == 'AIRPLAY'):
			if (source == 'AIRPLAY'): source = 'AirPlay'
			xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><List_Control><Cursor>'+val+'</Cursor></List_Control></'+source+'></YAMAHA_AV>'
		else:
			xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Cursor_Control><Cursor>'+val+'</Cursor></Cursor_Control></Main_Zone></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putPage(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'AIRPLAY'): source = 'AirPlay'
		xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><List_Control><Page>'+val+'</Page></List_Control></'+source+'></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putDirSelLine(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'AIRPLAY'): source = 'AirPlay'
		xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><List_Control><Direct_Sel>'+val+'</Direct_Sel></List_Control></'+source+'></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putTransport(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'AIRPLAY'): source = 'AirPlay'
		xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><Play_Control><Playback>'+val+'</Playback></Play_Control></'+source+'></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putShuffle(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'AIRPLAY'): source = 'AirPlay'
		xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><Play_Control><Play_Mode><Shuffle>'+val+'</Shuffle></Play_Mode></Play_Control></'+source+'></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putRepeat(self, dev, val, source):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		if (source == 'AIRPLAY'): source = 'AirPlay'
		xml_string = '<YAMAHA_AV cmd="PUT"><'+source+'><Play_Control><Play_Mode><Repeat>'+val+'</Repeat></Play_Mode></Play_Control></'+source+'></YAMAHA_AV>'
		root = xmitToReceiver( dev, xml_string)
		self.updateStatus(dev)

	def putBand(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Tuner><Play_Control><Tuning><Band>'+val+'</Band></Tuning></Play_Control></Tuner></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putStereo(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Tuner><Play_Control><FM_Mode>'+val+'</FM_Mode></Play_Control></Tuner></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putPresetChange(self, dev, val):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Tuner><Play_Control><Preset><Preset_Sel>'+val+'</Preset_Sel></Preset></Play_Control></Tuner></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)

	def putChSearch(self, dev, val, band):
		if dev is None:
			self.debugLog(u'no device defined')
			return
		if val is None:
			self.debugLog(u'value not defined')
			return
		xml_string = '<YAMAHA_AV cmd="PUT"><Tuner><Play_Control><Tuning><Freq><'+band+'><Val>'+val+'</Val></'+band+'></Freq></Tuning></Play_Control></Tuner></YAMAHA_AV>'
		root = xmitToReceiver(dev, xml_string)
		self.updateStatus(dev)






	# actions go here
	def getStatus(self, pluginAction, dev):
		self.updateStatus(dev)

	def setMute(self, pluginAction, dev):
		val = pluginAction.props['ddlmute']
		self.putMute(dev, val)

	def toggleMute(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if dev.states['mute']=='Off' else 'Off'
		self.putMute(dev, val)

	def setVolume(self, pluginAction, dev):
		val = pluginAction.props['txtvolume']
		self.putVolume(dev, val)

	def increaseVolume(self, pluginAction, dev):
		self.updateStatus(dev)
		val = str(int(dev.states['volume']) + int(pluginAction.props['txtincrement']))
		self.putVolume(dev, val)

	def decreaseVolume(self, pluginAction, dev):
		self.updateStatus(dev)
		val = str(int(dev.states['volume']) - int(pluginAction.props['txtincrement']))
		self.putVolume(dev, val)

	def setSwtrim(self, pluginAction, dev):
		val = int(pluginAction.props['txtswtrim'])
		if val > 60: val = 60
		if val < -60: val = -60
		val = str(int(val))
		self.putSwtrim(dev, val)

	def increaseSwtrim(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['swtrim']) + int(pluginAction.props['txtswincrement'])
		if val > 60: val = 60
		val = str(int(val))
		self.putSwtrim(dev, val)

	def decreaseSwtrim(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['swtrim']) - int(pluginAction.props['txtswincrement'])
		if val < -60: val = -60
		val = str(int(val))
		self.putSwtrim(dev, val)

	def setPower(self, pluginAction, dev):
		val = pluginAction.props['ddlpower']
		self.putPower(dev, val)

	def togglePower(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['power']=='Standby') else 'Standby'
		self.putPower(dev, val)

	def setSleep(self, pluginAction, dev):
		val = pluginAction.props['ddlsleep'].replace('n','')
		self.putSleep(dev, val)

	def setInput(self, pluginAction, dev):
		if (pluginAction.props['newinput'] == 'airplay'):
			val = 'AirPlay'
		elif (pluginAction.props['newinput'] == 'spotify'):
			val = 'Spotify'
		elif (pluginAction.props['newinput'] == 'napster'):
			val = 'Napster'
		else:
			val = pluginAction.props['newinput'].upper().replace('.','/').replace('_',' ')
		self.putInput(dev, val)

	def setScene(self, pluginAction, dev):
		val = pluginAction.props['scene']
		self.putScene(dev, val)

	def setEnhancer(self, pluginAction, dev):
		val = pluginAction.props['enh']
		self.putEnhancer(dev, val)

	def toggleEnhancer(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['dspenh']=='Off') else 'Off'
		self.putEnhancer(dev, val)

	def setStraight(self, pluginAction, dev):
		val = pluginAction.props['straight']
		self.putStraight(dev, val)

	def toggleStraight(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['dspstraight']=='Off') else 'Off'
		self.putStraight(dev, val)

	def setDSPProg(self, pluginAction, dev):
		if (pluginAction.props['newdspprog'] == 'twoch_Stereo'):
			val = '2ch Stereo'
		elif (pluginAction.props['newdspprog'] == 'sevench_Stereo'):
			val = '7ch Stereo'
		else:
			val = pluginAction.props['newdspprog'].replace('_',' ')
		self.putDSPProg(dev, val)

	def set3dcinema(self, pluginAction, dev):
		val = pluginAction.props['threedcinema']
		self.put3dcinema(dev, val)

	def toggle3dcinema(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'Auto' if (dev.states['dsp3dcinema']=='Off') else 'Off'
		self.put3dcinema(dev, val)

	def setBass(self, pluginAction, dev):
		val = int(pluginAction.props['txtbass'])
		if val > 60: val = 60
		if val < -60: val = -600
		val = str(int(val))
		self.putBass(dev, val)

	def increaseBass(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['bass']) + int(pluginAction.props['txtincbass'])
		if val > 60: val = 60
		val = str(int(val))
		self.putBass(dev, val)

	def decreaseBass(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['bass']) - int(pluginAction.props['txtdecbass'])
		if val < -60: val = -60
		val = str(int(val))
		self.putBass(dev, val)

	def setTrebble(self, pluginAction, dev):
		val = int(pluginAction.props['txttrebble'])
		if val > 60: val = 60
		if val < -60: val = -600
		val = str(int(val))
		self.putTrebble(dev, val)

	def increaseTrebble(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['trebble']) + int(pluginAction.props['txtinctrebble'])
		if val > 60: val = 60
		val = str(int(val))
		self.putTrebble(dev, val)

	def decreaseTrebble(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['trebble']) - int(pluginAction.props['txtdectrebble'])
		if val < -60: val = -60
		val = str(int(val))
		self.putTrebble(dev, val)

	def setPuredirect(self, pluginAction, dev):
		val = pluginAction.props['txtpuredirect']
		self.putPuredirect(dev, val)

	def togglePuredirect(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['puredirect']=='Off') else 'Off'
		self.putPuredirect(dev, val)

	def setHdmiout1(self, pluginAction, dev):
		val = pluginAction.props['txtho1']
		self.putHdmiout1(dev, val)

	def toggleHdmiout1(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['hdmiout1']=='Off') else 'Off'
		self.putHdmiout1(dev, val)

	def setHdmiout2(self, pluginAction, dev):
		val = pluginAction.props['txtho2']
		self.putHdmiout2(dev, val)

	def toggleHdmiout2(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'On' if (dev.states['hdmiout2']=='Off') else 'Off'
		self.putHdmiout2(dev, val)

	def setDlglift(self, pluginAction, dev):
		val = int(pluginAction.props['dlglift'])
		if val > 5: val = 5
		if val < 0: val = 0
		val = str(int(val))
		self.putDlglift(dev, val)

	def increaseDlglift(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['dialoguelift']) + int(pluginAction.props['incdlglift'])
		if val > 5: val = 5
		val = str(int(val))
		self.putDlglift(dev, val)

	def decreaseDlglift(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['dialoguelift']) - int(pluginAction.props['decdlglift'])
		if val < 0: val = 0
		val = str(int(val))
		self.putDlglift(dev, val)

	def setDlglvl(self, pluginAction, dev):
		val = int(pluginAction.props['dlglvl'])
		if val > 3: val = 3
		if val < 0: val = 0
		val = str(int(val))
		self.putDlglvl(dev, val)

	def increaseDlglvl(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['dialoguelvl']) + int(pluginAction.props['incdlglvl'])
		if val > 3: val = 3
		val = str(int(val))
		self.putDlglvl(dev, val)

	def decreaseDlglvl(self, pluginAction, dev):
		self.updateStatus(dev)
		val = int(dev.states['dialoguelvl']) - int(pluginAction.props['decdlglvl'])
		if val < 0: val = 0
		val = str(int(val))
		self.putDlglvl(dev, val)

	def setAdaptivedrc(self, pluginAction, dev):
		val = pluginAction.props['adrc']
		self.putAdaptivedrc(dev, val)

	def toggleAdaptivedrc(self, pluginAction, dev):
		self.updateStatus(dev)
		val = 'Auto' if (dev.states['adaptivedrc']=='Off') else 'Off'
		self.putAdaptivedrc(dev, val)

	def setMenu(self, pluginAction, dev):
		val = pluginAction.props['ddlmenu'].replace('_',' ')
		self.putMenu(dev, val)

	def setCursor(self, pluginAction, dev):
		source = dev.states['input'].upper()
		val = pluginAction.props['ddlcursor']
		self.putCursor(dev, val, source)

	def setPage(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY' or source == 'NET_RADIO'):
			val = pluginAction.props['ddlpage']
			self.putPage(dev, val, source)

	def setDirSelLine(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY' or source == 'NET_RADIO'):
			val = 'Line_'+str(int(pluginAction.props['ddllinesel'].replace('s', '')))
			self.putDirSelLine(dev, val, source)

	def setTransport(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY' or source == 'NET_RADIO'):
			val = pluginAction.props['ddltrans'].replace('_', ' ')
			self.putTransport(dev, val, source)

	def togglePlayPause(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY'):
			self.updateStatus(dev)
			val = 'Play' if (dev.states['playback']=='Pause') else 'Pause'
			self.putTransport(dev, val, source)

	def setShuffle(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY'):
			val = pluginAction.props['ddlshuffle']
			self.putShuffle(dev, val, source)

	def toggleShuffle(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY'):
			self.updateStatus(dev)
			val = 'On' if (dev.states['shuffle']=='Off') else 'Off'
			self.putShuffle(dev, val, source)

	def setRepeat(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY'):
			val = pluginAction.props['ddlrepeat']
			self.putRepeat(dev, val, source)

	def toggleRepeat(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'SERVER' or source == 'USB' or source == 'AIRPLAY'):
			self.updateStatus(dev)
			if (dev.states['repeat'] == 'Off'):
				val = 'One'
			elif (dev.states['repeat'] == 'One'):
				val = 'All'
			else:
				val = 'Off'
			self.putRepeat(dev, val, source)

	def setBand(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			val = pluginAction.props['selband']
			self.putBand(dev, val)

	def toggleBand(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			self.updateStatus(dev)
			val = 'FM' if (dev.states['band']=='AM') else 'AM'
			self.putBand(dev, val)

	def setStereo(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			val = pluginAction.props['selstereo']
			self.putStereo(dev, val)

	def toggleStereo(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			self.updateStatus(dev)
			val = 'Assert' if (dev.states['stereo']=='Negate') else 'Negate'
			self.putStereo(dev, val)

	def presetChange(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			val = pluginAction.props['prech']
			self.putPresetChange(dev, val)

	def chSearch(self, pluginAction, dev):
		source = dev.states['input'].upper()
		if (source == 'TUNER'):
			val = pluginAction.props['search'].replace('_', ' ')
			band = dev.states['band'].upper()
			self.putChSearch(dev, val, band)
