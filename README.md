indigo-yamaharx
===============

[Indigo](http://www.perceptiveautomation.com/indigo/index.html) plugin - basic control of Yamaha RX series a/v receivers

### Requirements

1. [Indigo 6](http://www.perceptiveautomation.com/indigo/index.html) or later (pro version only)
2. Yamaha RX-Vx75 Series A/V Receiver (needs to be accessible via network from the box hosting your Indigo server)

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
* Set Input
* Set Scene
* Set Bass
* Increase Bass
* Decrase Bass
* Set Trebble
* Increase Trebble
* Decrease Trebble
* Set SW-Trim
* Increase SW-Trim
* Decrease SW-Trim
* Set DialogueLift
* Increase DialogueLift
* Decrease DialogueLift
* Set DialogueLevel
* Increase DialogueLevel
* Decrease DialogueLevel
* Set DSP Program
* Set DSP Enhancer
* Toggle DSP Enhancer
* Set DSP 3D Cinema
* Toggle DSP 3D Cinema
* Set PureDirect
* Toggle PureDirect
* Set Adaptive DRC
* Toggle Adaptive DRC
* Set HDMI Out 1
* Toggle HDMI Out 1
* Set HDMI Out 2
* Toggle HDMI Out 2
* Set Transport (Play/Pause/Stop/Skip Rev/Skip Fwd)
* Toggle Play/Pause
* Set Repeat
* Toggle Repeat
* Set Shuffle
* Toggle Shuffle
* Set Line
* Set Page
* Set Band (Tuner: FM/AM)
* Toggle Band (Tuner: FM/AM)
* Set Stereo (Tuner)
* Toggle Stereo (Tuner)
* Change Preset (Tuner: Up/Down)
* Search Channel (Tuner: Down/Up/Auto Down/Auto Up)
* Get Status

### States Surfaced
* power (On, Standby)
* sleep (Off,30,60,90,120)
* volume (int)
* mute (bool)
* bass (int)
* trebble (int)
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
