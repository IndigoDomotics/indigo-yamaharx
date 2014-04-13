indigo-yamaharx
===============

[Indigo](http://www.perceptiveautomation.com/indigo/index.html) plugin - basic control of Yamaha RX series a/v receivers

### Requirements

1. [Indigo 6](http://www.perceptiveautomation.com/indigo/index.html) or later (pro version only)
2. Yamaha RX-V Series A/V Receiver (needs to be accessible via network from the box hosting your Indigo server)

### Installation Instructions

1. Download latest release [here](https://github.com/discgolfer1138/indigo-yamaharx/releases)
2. Follow [standard plugin installation process](http://bit.ly/1e1Vc7b)

### Compatible Hardware

while the plugin may be compatible with other models, it has only been tested on the following:

* Yamaha RX-V3900
* Yamaha RX-Vx75

### Actions Supported
* Set/Toggle Power
* Set/Increase/Decrease Volume
* Set/Toggle Mute
* Set Sleep
* Set Input
* Set Scene
* Set/Increase/Decrease Bass
* Set/Increase/Decrease Treble
* Set/Increase/Decrease SW-Trim
* Set/Increase/Decrease DialogueLift
* Set/Increase/Decrease DialogueLevel
* Set DSP Program
* Set/Toggle DSP Enhancer
* Set/Toggle DSP 3D Cinema
* Set/Toggle PureDirect
* Set/Toggle Adaptive DRC
* Set/Toggle HDMI Out 1
* Set/Toggle HDMI Out 2
* Set Transport (Play/Pause/Stop/Skip Rev/Skip Fwd)
* Toggle Play/Pause
* Set/Toggle Repeat
* Set/Toggle Shuffle
* Set Line
* Set Page
* Set/Toggle Band (Tuner: FM/AM)
* Set/Toggle Stereo (Tuner)
* Change Preset (Tuner: Up/Down)
* Search Channel (Tuner: Down/Up/Auto Down/Auto Up)
* Get Status

### States Surfaced
* power (On, Standby)
* sleep (Off,30,60,90,120)
* volume (int)
* mute (bool)
* bass (int)
* treble (int)
* SW-trim
* dialogue lift
* dialogue level
* DSP program
* DSP enhancer
* DSP 3D Cinema
* PureDirect
* Adaptive DRC
* HDMI Out 1
* HDMI Out 2
* transport (Play/Pause/Stop/Off)
* repeat
* shuffle
* artist
* album
* song
* listname
* line 1-8
* selected line
* page
* input (HDMI1, HDMI2, HDMI3, HDMI4, HDMI5, AirPlay, NET RADIO, SERVER, USB, TUNER, V-AUX, Spotify, Napster, AV1, AV2, AV3, AV4, AV5, AV6, AUDIO1, AUDIO2, PHONO)
* band (Tuner)
* stereo (Tuner)
* frequency (Tuner)
* program service (Tuner) = artist
* program type (Tuner) = artist
* radiotext A (Tuner) = album
* radiotext B (Tuner) = song
