indigo-yamaharx
===============

[Indigo](http://www.perceptiveautomation.com/indigo/index.html) plugin - basic control of Yamaha RX series a/v receivers

### Requirements

1. [Indigo 6](http://www.perceptiveautomation.com/indigo/index.html) or later (pro version only)
2. Yamaha RX Series A/V Receiver (needs to be accessible via network from the box hosting your Indigo server)

### Installation Instructions

1. Download latest release [here](https://github.com/discgolfer1138/indigo-yamaharx/releases)
2. Follow [standard plugin installation process](http://bit.ly/1e1Vc7b)

### Compatible Hardware
This plugin has only been tested with the Yamaha RX-V3900

### Actions Supported
* Set Volume
* Increase Volume
* Decrease Volume
* Set Mute
* Toggle Mute
* Set Power
* Toggle Power
* Set Sleep
* Get Status

### States Surfaced
* power (On, Standby)
* sleep (Off,30,60,90,120)
* volume (int)
* mute (bool)
* input (sirius, xm, tuner, multi_ch, phono, cd, tv, md.cd-r, bd.hd_dvd, dvd, cbl.sat, dvr, vcr, v-aux, dock, pc.mcx, net_radio, rhapsody, usb)
