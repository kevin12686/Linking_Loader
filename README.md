# Linking_Loader

Object Program : LINK1IN.DAT

Beginning Address : 4000
```
Load Map :

Control      Symbol
Section      Name         Address      Length
---------------------------------------------
PROGA                     4000         63
             LISTA        4040
             ENDA         4054
PROGB                     4063         7F
             LISTB        40C3
             ENDB         40D3
PROGC                     40E2         51
             LISTC        4112
             ENDC         4124

Memory Address :

Memory
Address   Contents
----------------------------------------------
3FF0      xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
4000      -------- -------- -------- --------
4010      -------- -------- -------- --------
4020      03201D77 1040C705 0014---- --------
4030      -------- -------- -------- --------
4040      -------- -------- -------- --------
4050      -------- 10412600 00080040 51000004
4060      100083-- -------- -------- --------
4060      -------- -------- -------- --------
4070      -------- -------- -------- --------
4080      -------- -------- -------- --------
4090      -------- -------- --031040 40772027
40A0      05100014 -------- -------- --------
40A0      -------- -------- -------- --------
40B0      -------- -------- -------- --------
40C0      -------- -------- -------- --------
40D0      ------10 41260000 08004051 00000410
40E0      0083---- -------- -------- --------
40E0      -------- -------- -------- --------
40F0      -------- -------- ----0310 40407710
4100      40C70510 0014---- -------- --------
4100      -------- -------- -------- --------
4110      -------- -------- -------- --------
4120      -------- 10412600 00080040 51000004
```
