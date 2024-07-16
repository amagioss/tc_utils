

# TC Utils

This repo has utility packages in python, golang to convert between media timecodes. Timecodes
can be in one of the following formats:

- SMPTE (HH:MM:SS:FF(non-drop frame) or HH:MM:SS;FF(drop frame))
- Normal Playout time (HH:MM:SS.nnn)
- Float (seconds)


## Python Usage

`pip install https://github.com/amagioss/tc_utils/py`

```python
import tc_utils

# Returns: 4803.466666666666
tc_utils.ParseTimeStr("01:20:03:14", tc_utils.Rate_30)

# Returns: 4803.47013680347
tc_utils.ParseTimeStr("01:20:03;14", tc_utils.Rate_29_97)

# Returns: '01:20:03;14'
tc_utils.GetTimeStr(4803.470, tc_utils.SmpteTimecode, rate=tc_utils.Rate_29_97)

# Returns: '01:20:03:14'
tc_utils.GetTimeStr(4803.470, tc_utils.SmpteTimecode, rate=tc_utils.Rate_30) 
```


## Golang

Dervied from the original code present in https://github.com/spiretechnology/go-timecode


## Javascript

Derived from the original code present in https://github.com/spiretechnology/js-timecode
