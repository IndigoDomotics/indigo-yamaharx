#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import traceback

# import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout

import rxv
from rxv import exceptions as rxv_exceptions

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from xml.etree.ElementTree import ParseError

try:
    import indigo
except:
    pass

kSleepBetweenUpdatePolls = 2   # number of seconds to sleep between polling each receiver for current status
kSleepValueMap = {
    "Off": "Off",
    "120 min": "n120",
    "90 min": "n90",
    "60 min": "n60",
    "30 min": "n30",
}

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "on")


class ClassicReceiver(object):
    kInputList = (
        ('tuner', 'TUNER'),
        ('multi_ch', 'MULTI CH'),
        ('phono', 'PHONO'),
        ('cd', 'CD'),
        ('tv', 'TV'),
        ('md.cd-r', 'MD/CD-R'),
        ('bd.hd_dvd', 'BD/HD DVD'),
        ('dvd', 'DVD'),
        ('cbl.sat', 'CBL/SAT'),
        ('dvr', 'DVR'),
        ('vcr', 'VCR'),
        ('v-aux', 'V-AUX'),
        ('dock', 'DOCK'),
        ('pc.mcx', 'PC/MCX'),
        ('net_radio', 'NET RADIO'),
        ('usb', 'USB'),
    )
    @staticmethod
    def xmitToReceiver(dev, xml_string):
        url = 'http://' + dev.pluginProps['txtip'] + '/YamahaRemoteControl/ctrl'

        req = urllib.request.Request(
            url=url,
            data=xml_string,
            headers={'Content-Type': 'application/xml'})
        resp = urllib.request.urlopen(req)
        status_xml = resp.read()
        root = ET.fromstring(status_xml)
        return root

    @staticmethod
    def putMute(logger, dev, val):
        if dev is None:
            logger.debug("no device defined")
            return

        if val is None:
            logger.debug("value not defined")
            return

        xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Mute>'+val+'</Mute></Vol></Main_Zone></YAMAHA_AV>'
        root = ClassicReceiver.xmitToReceiver( dev, xml_string)

    @staticmethod
    def putVolume(logger, dev, val):
        if dev is None:
            logger.debug("no device defined")
            return

        if val is None:
            logger.debug("value not defined")
            return

        xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>'+val+'</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>'
        root = ClassicReceiver.xmitToReceiver( dev, xml_string)

    @staticmethod
    def putPower(logger, dev, val):
        if dev is None:
            logger.debug("no device defined")
            return

        if val is None:
            logger.debug("value not defined")
            return

        xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>'+val+'</Power></Power_Control></Main_Zone></YAMAHA_AV>'
        root = ClassicReceiver.xmitToReceiver( dev, xml_string)

    @staticmethod
    def putSleep(logger, dev, val):
        if dev is None:
            logger.debug("no device defined")
            return

        if val is None:
            logger.debug("value not defined")
            return

        xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Sleep>'+val+'</Sleep></Power_Control></Main_Zone></YAMAHA_AV>'
        root = ClassicReceiver.xmitToReceiver( dev, xml_string)

    @staticmethod
    def putInput(logger, dev, val):
        if dev is None:
            logger.debug("no device defined")
            return

        if val is None:
            logger.debug("value not defined")
            return

        xml_string = '<YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>'+val+'</Input_Sel></Input></Main_Zone></YAMAHA_AV>'
        root = ClassicReceiver.xmitToReceiver( dev, xml_string)


class Plugin(indigo.PluginBase):

    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get("showDebugInfo", False)
        self.devices = {}
        self.refresh_receiver_list()

    ##################################
    # Standard plugin operation methods
    ##################################
    def startup(self):
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

    def device_start_comm(self, dev):
        if dev.deviceTypeId == "receiver":
            devTup = (dev,)
        elif dev.deviceTypeId == "rxvX73":
            try:
                rxv_obj = self.receivers.get(dev.pluginProps["control-url"], None)
                if not rxv_obj and len(dev.pluginProps["manual-ip"]):
                    rxv_obj = rxv.RXV(ctrl_url=dev.pluginProps["manual-ip"])
                devTup = (dev, rxv_obj)
            except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
                dev.setErrorStateOnServer('unavailable')
                if isinstance(e, ConnectTimeout) or  isinstance(e, ReadTimeout):
                    self.logger.debug(f"device '{dev.name}' connection timed out")
                else:
                    self.logger.debug(f"device '{dev.name}' had a connection error")
                return
            except ParseError:
                # This seems to happen relatively frequently - apparently sometimes the amp goes out to lunch for
                # a bit (causing connection errors) and when it comes back it doesn't always return correct XML.
                # I think the better idea here is to just pass on these errors as it always seems to resolve itself.
                dev.setErrorStateOnServer('unavailable')
                devTup = (dev, None)
            except Exception as e:
                self.logger.error(f"Couldn't start device {dev.name} - it may not be available on the network or the IP address may have changed.")
                self.logger.debug(f"exception starting device:\n{traceback.format_exc(10)}")
                return
        self.devices[dev.id] = devTup
        self.updateStatus(dev.id)

    def device_stop_comm(self, dev):
        try:
            del self.devices[dev.id]
        except:
            pass

    def run_concurrent_thread(self):
        try:
            while True:
                for devId in list(self.devices.keys()):
                    self.updateStatus(devId)
                self.sleep(2)
        except self.StopThread:
            return
        except Exception as e:
            self.logger.error(f"runConcurrentThread error: \n{traceback.format_exc(10)}")

    ##################################
    # Config dialog methods
    ##################################
    ###############
    # get_receiver_list
    #
    # Returns the list of receivers as a tuple for the device config dialog.
    ###############
    def get_receiver_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        return [(k, v.friendly_name) for k, v in self.receivers.items()]

    def get_input_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        dev = indigo.devices.get(targetId, None)
        if dev.deviceTypeId == 'receiver':
            return ClassicReceiver.kInputList
        elif dev.deviceTypeId == "rxvX73":
            dev, rxv_obj = self.devices.get(dev.id, (None, None))
            if rxv_obj:
                return [(k.replace("iPod (USB)", "iPod").replace(" ", "_"), k) for k in list(rxv_obj.inputs().keys())]
            return []

    def get_zone_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        dev = indigo.devices.get(targetId, None)
        d, rxv_obj = self.devices.get(dev.id, (None, None))
        if rxv_obj:
            return [(k, k) for k in rxv_obj.zones()]
        return []

    ########################################
    # Prefs dialog methods
    ########################################
    def closed_prefs_config_ui(self, valuesDict, userCancelled):
        # Since the dialog closed we want to set the debug flag - if you don't directly use
        # a plugin's properties (and for debugLog we don't) you'll want to translate it to
        # the appropriate stuff here.
        if not userCancelled:
            self.debug = valuesDict.get("showDebugInfo", False)
            if self.debug:
                indigo.server.log("Debug logging enabled")
            else:
                indigo.server.log("Debug logging disabled")

    ##################################
    # Helper methods
    ##################################

    ###############
    # refresh_receiver_list
    #
    # Refreshes the self.receivers list from the SSDP query. It's automatically loaded at plugin launch, but we provide
    # this method just in case we need to refresh the list. We also have a button in the config dialog that calls this
    # so that we can force the list to refresh in the dialog itself. We don't refresh automatically because it takes
    # a couple of seconds for the method to finish so the dialog looks like it's hung up.
    ###############
    def refresh_receiver_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        self.receivers = {r.ctrl_url: r for r in rxv.find()}
        self.logger.debug(f"receivers list: {str(self.receivers)}")

    ###############
    # updateStatus
    #
    # Updates the status for the specified device.
    ###############
    def update_status(self, dev_id):
        devTup = self.devices.get(dev_id, None)
        if devTup:
            dev = devTup[0]
            if dev.deviceTypeId == "receiver":
                xml_string = '<YAMAHA_AV cmd="GET"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>'
                root = ClassicReceiver.xmitToReceiver(dev, xml_string)
                power = root.find("./Main_Zone/Basic_Status/Power_Control/Power").text
                sleep = root.find("./Main_Zone/Basic_Status/Power_Control/Sleep").text
                if(sleep!='Off'): sleep = "n"+sleep
                volume = root.find("./Main_Zone/Basic_Status/Vol/Lvl/Val").text
                mute = root.find("./Main_Zone/Basic_Status/Vol/Mute").text
                inputmode = root.find("./Main_Zone/Basic_Status/Input/Input_Sel").text
                state_list = [
                    {"key": "power", "value": power},
                    {"key": "sleep", "value": sleep},
                    {"key": "volume", "value": volume},
                    {"key": "mute", "value": mute},
                    {"key": "input", "value": inputmode}
                ]
                dev.updateStatesOnServer(state_list)
            elif dev.deviceTypeId == "rxvX73":
                rxv_obj = devTup[1]
                if not rxv_obj:
                    self.refresh_receiver_list()
                    rxv_obj = self.receivers.get(dev.pluginProps["control-url"], None)
                    if not rxv_obj:
                        dev.setErrorStateOnServer("unavailable")
                        return
                    else:
                        self.devices[dev.id] = (dev, rxv_obj)
                try:
                    status = rxv_obj.basic_status
                    state_list = [
                        {"key": "power", "value": status.on},
                        {"key": "volume", "value": status.volume},
                        {"key": "mute", "value": status.mute},
                        {"key": "input", "value": status.input.replace(" ", "_")}
                    ]
                    dev.updateStatesOnServer(state_list)
                    dev.updateStateOnServer(key="sleep", value=kSleepValueMap[rxv_obj.sleep])
                    if dev.errorState:
                        dev.setErrorStateOnServer(None)
                except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
                    dev.setErrorStateOnServer('unavailable')
                    if isinstance(e, ConnectTimeout) or isinstance(e, ReadTimeout):
                        self.logger.debug(f"device '{dev.name}' connection timed out")
                    else:
                        self.logger.debug(f"device '{dev.name}' had a connection error")
                except ParseError:
                    # dev.setErrorStateOnServer('unavailable')
                    # self.logger.debug(f"device '{dev.name}' failed to update status with an XML parse error")
                    # This seems to happen relatively frequently - apparently sometimes the amp goes out to lunch for
                    # a bit (causing connection errors) and when it comes back it doesn't always return correct XML.
                    # I think the better idea here is to just pass on these errors as it always seems to resolve itself.
                    pass
                except Exception as e:
                    dev.setErrorStateOnServer('unavailable')
                    self.logger.debug(f"device '{dev.name}' failed to update status with error: \n{traceback.format_exc(10)}")

    ###############
    # _set_rxv_property
    #
    # Updates the specified property for the specified device. It catches exceptions and does the appropriate thing.
    ###############
    def _set_rxv_property(self, dev, property, value):
        try:
            d, rxv_obj = self.devices.get(dev.id, (None, None))
            if rxv_obj:
                if callable(getattr(rxv_obj, property)):
                    if value:
                        getattr(rxv_obj, property)(value)
                    else:
                        getattr(rxv_obj, property)()
                else:
                    setattr(rxv_obj, property, value)
            else:
                self.logger.error(f"device '{dev.name}' isn't available")
        except (ConnectTimeout, ReadTimeout, ConnectionError) as e:
            dev.setErrorStateOnServer('unavailable')
            if isinstance(e, ConnectTimeout) or  isinstance(e, ReadTimeout):
                self.logger.debug(f"device '{dev.name}' connection timed out")
                self.logger.error(f"device '{dev.name}' is unavailable")
            else:
                self.logger.debug(f"device '{dev.name}' had a connection error")
                self.logger.error(f"device '{dev.name}' is unavailable")
        except rxv_exceptions.ResponseException as e:
            response = ET.XML(str(e))
            if response.get("RC") == "3":
                # RC 3 is what happens when you issue a command that's not valid - wrong menu navigation direction, etc.
                # We just skip it.
                pass
            elif response.get("RC") != "4":
                self.logger.error(f"device '{dev.name}' can't have property '{property}' set to value '{str(value)}'")
            else:
                # RC 4 is what happens when the amp is offline or in standby and you try to send it a command other than
                # to turn on (if in standby)
                self.logger.error(f"device '{dev.name}' is unavailable")
        except ET.ParseError:
            # dev.setErrorStateOnServer('unavailable')
            # self.logger.debug(f"device '{dev.name}' failed to update status with an XML parse error")
            # This seems to happen relatively frequently - apparently sometimes the amp goes out to lunch for
            # a bit (causing connection errors) and when it comes back it doesn't always return correct XML.
            # I think the better idea here is to just pass on these errors as it always seems to resolve itself.
            pass
        except:
            dev.setErrorStateOnServer('unavailable')
            self.logger.error(f"device '{dev.name}' failed to set property status with error: \n{traceback.format_exc(10)}")

    ##################################
    # Action methods
    ##################################
    def getStatus(self, pluginAction, dev):
        self.updateStatus(dev.id)

    def setMute(self, pluginAction, dev):
        self.logger.debug("setMute called")
        val = pluginAction.props['ddlmute']
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putMute(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'mute', str2bool(val))

    def toggleMute(self, pluginAction, dev):
        self.logger.debug("toggleMute called")
        self.updateStatus(dev.id)
        dev.refreshFromServer()
        if dev.deviceTypeId == "receiver":
            val = 'On' if dev.states['mute'] == 'Off' else 'Off'
            ClassicReceiver.putMute(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'mute', not str2bool(dev.states['mute']))

    def setVolume(self, pluginAction, dev):
        self.logger.debug("setVolume called")
        val = pluginAction.props['txtvolume']
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putVolume(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'volume', float(val))

    def increaseVolume(self, pluginAction, dev):
        self.logger.debug("increaseVolume called")
        self.updateStatus(dev.id)
        dev.refreshFromServer()
        val = float(dev.states['volume']) + int(pluginAction.props['txtincrement'])
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putVolume(self.logger, dev, int(val))
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'volume', val)

    def decreaseVolume(self, pluginAction, dev):
        self.logger.debug("decreaseVolume called")
        self.updateStatus(dev.id)
        dev.refreshFromServer()
        val = float(dev.states['volume']) - int(pluginAction.props['txtincrement'])
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putVolume(self.logger, dev, int(val))
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'volume', val)

    def setPower(self, pluginAction, dev):
        self.logger.debug("setPower called")
        val = pluginAction.props['ddlpower']
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putPower(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'on', str2bool(val))

    def togglePower(self, pluginAction, dev):
        self.logger.debug("togglePower called")
        self.updateStatus(dev.id)
        dev.refreshFromServer()
        val = 'On' if (dev.states['power']=='Standby') else 'Standby'
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putPower(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'on', str2bool(val))

    def setSleep(self, pluginAction, dev):
        self.logger.debug("setSleep called")
        val = pluginAction.props['ddlsleep'].replace('n','')
        if dev.deviceTypeId == "receiver":
            ClassicReceiver.putSleep(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'sleep', "Off" if val == "Off" else f"{val} min")

    def setInput(self, pluginAction, dev):
        self.logger.debug("setInput called")
        if dev.deviceTypeId == "receiver":
            val = pluginAction.props['ddlinput'].upper().replace(".","/").replace("_"," ")
            ClassicReceiver.putInput(self.logger, dev, val)
        elif dev.deviceTypeId == "rxvX73":
            self._set_rxv_property(dev, 'input', pluginAction.props['ddlinput'].replace("_", " ").replace("iPod", "iPod (USB)"))

    def setZone(self, pluginAction, dev):
        self.logger.debug("setZone called")
        self._set_rxv_property(dev, 'zone', pluginAction.props['zone'])

    def playNetRadio(self, pluginAction, dev):
        self.logger.debug("playNetRadio called")
        self._set_rxv_property(dev, 'net_radio', pluginAction.props['path'])

    def menuUp(self, pluginAction, dev):
        self.logger.debug("menuUp called")
        self._set_rxv_property(dev, 'menu_up', None)

    def menuDown(self, pluginAction, dev):
        self.logger.debug("menuDown called")
        self._set_rxv_property(dev, 'menu_down', None)

    def menuLeft(self, pluginAction, dev):
        self.logger.debug("menuLeft called")
        self._set_rxv_property(dev, 'menu_left', None)

    def menuRight(self, pluginAction, dev):
        self.logger.debug("menuRight called")
        self._set_rxv_property(dev, 'menu_right', None)

    def menuSelect(self, pluginAction, dev):
        self.logger.debug("menuSelect called")
        self._set_rxv_property(dev, 'menu_sel', None)

    def menuReturn(self, pluginAction, dev):
        self.logger.debug("menuReturn called")
        self._set_rxv_property(dev, 'menu_return', None)