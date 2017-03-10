indigo-yamaharx
===============

This is a plugin for the [Indigo](http://www.indigodomo.com/) smart home server that integrates the Yamaha RX-V series 
A/V receivers. The receiver must have some kind of network connection (wired Ethernet, WiFi). Serial control is not 
supported.

### Requirements

1. [Indigo 7](http://www.indigodomo.com/) or later
2. Yamaha RX-V Series A/V Receiver (needs to be accessible via network from the box hosting your Indigo server)

### Installation Instructions

1. Download latest release [here](https://github.com/IndigoDomotics/indigo-yamaharx/releases). If you're using Indigo 6, 
you can download the [0.1.1 release](https://github.com/IndigoDomotics/indigo-yamaharx/releases/tag/0.1.1) instead, but 
note that it only supports the RX-V3900. Support for newer receivers requires v1.0.0 or later.
2. Follow [standard plugin installation process](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:getting_started#installing_plugins_configuring_plugin_settings_permanently_removing_plugins)

### Compatible Hardware
This plugin supports both the RX-V3900 and the RX-Vx73 (RX-V473, RX-V573, RX-V673, RX-V773) receiver line. Other 
Yahama RX-V receivers that use the same command API may also work.

### Usage

Select the appropriate receiver when creating a new receiver in Indigo. If you choose RX-Vx73, the config dialog should 
show a popup with the available receivers on your network. If your network doesn't show in the list, it may be because 
it's not configured to operate in network standby mode. Confirm that Network Standby is turned on. If that doesn't solve 
the issue, you may manually specify the IP address for the receiver (your router may be blocking the discovery protocol).

### Actions Supported by All Receivers
* Set Volume
* Increase Volume
* Decrease Volume
* Set Mute
* Toggle Mute
* Set Power
* Toggle Power
* Set Sleep
* Get Status

### Additional Actions Supported by RX-Vx73 (and compatible) Receivers
* Set Zone - specify the zone that future commands will go to (where applicable) - untested until we have someone with a 
multizone amp to test against
* Menu Up, Menu Down, Menu Left, Menu Right, Menu Select, Menu Return - to navigate the menus when an input is selected 
that presents menus on the receiver itself. Note - in our testing, left/right don't work reliably, but using select and 
return seem to work consistently and do pretty much the same thing.
* Play Net Radio Station (Experimental) - specify the path to a network radio station (we've seen mixed results using 
the rxv library to do this - sometimes it works sometimes it doesn't)

### States Exposed
* power (On, Standby)
* sleep (Off,30,60,90,120)
* volume (float)
* mute (bool)
* input 
	* RX-V3900: (sirius, xm, tuner, multi_ch, phono, cd, tv, md.cd-r, bd.hd_dvd, dvd, cbl.sat, dvr, vcr, v-aux, dock, pc.mcx, net_radio, rhapsody, usb)
	* RX-Vx73: (based on receiver capability - input list is dynamically generated for the set input action)
	
### License

The original author of the plugin (discgolfer1138) did not apply a license, so there is none. v1.0.0 and later uses a 
modified version of the [rxv library](https://github.com/wuub/rxv) (included in the plugin and in this repo for ease of 
installation). See the LICENSE file in *Yamaha RX.indigoPlugin/Contents/Server Plugin/rxv* for details.

### rxv Library Changes

The included rxv library has the following changes:

* Added *timeout* to the RXV object that allows specification of a timeout value on all network communications. The 
default network timeout is 30 seconds which can cause significant delays in plugin processing so by shortening it to
5 seconds we can more quickly determine if a receiver is no longer available on the network and react accordingly.

### Troubleshooting

Sometimes the receiver's status will change to unavailable - this means that the plugin is having a problem communicating 
with it. This can happen for a variety of reasons, but one in particular seems to be an issue in our testing. When the 
network radio input is selected, it will periodically become busy, presumably trying to query for updated radio stations, 
and this will cause all other network communication to stop. So, apparently the receiver has a single network connection 
that it uses for everything. Unfortunately, we can't tell the difference between one of these times and when the receiver 
is actually offline (unplugged or otherwise unavailable on the network). 