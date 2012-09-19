indigo_yamahaav
===============

Indigo plugin to control Yamaha RXV3900 receivers

##adding a few notes to myself:
http://192.168.1.4/YamahaRemoteControl/ctrl

###to set volume to -35db
####Request
`<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>-350</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>`
####Response
`<YAMAHA_AV rsp="PUT" RC="0"><Main_Zone><Vol><Lvl></Lvl></Vol></Main_Zone></YAMAHA_AV>`

###to set volume to -30db
####Request
`<YAMAHA_AV cmd="PUT"><Main_Zone><Vol><Lvl><Val>-300</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Vol></Main_Zone></YAMAHA_AV>`
####Response
`<YAMAHA_AV rsp="PUT" RC="0"><Main_Zone><Vol><Lvl></Lvl></Vol></Main_Zone></YAMAHA_AV>`

###get system statys for main zone
####Request
`<YAMAHA_AV cmd="GET"><Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone></YAMAHA_AV>`
####Response
`<YAMAHA_AV rsp="GET" RC="0"><Main_Zone><Basic_Status><Power_Control><Power>On</Power><Sleep>Off</Sleep></Power_Control><Vol><Lvl><Val>-300</Val><Exp>1</Exp><Unit>dB</Unit></Lvl><Mute>Off</Mute></Vol><Input><Input_Sel>CBL/SAT</Input_Sel></Input><Surr><Pgm_Sel><Straight>Off</Straight><Pgm>Surround Decode</Pgm></Pgm_Sel></Surr></Basic_Status></Main_Zone></YAMAHA_AV>`