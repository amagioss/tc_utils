

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

# Returns: "smpte_timecode_non_drop"
tc_utils.GetTimecodeType("01:02:03:04")

# Returns: 4803.466666666666
tc_utils.ParseTimeStr("01:20:03:14", tc_utils.Rate_30)

# Returns: 4803.47013680347
tc_utils.ParseTimeStr("01:20:03;14", tc_utils.Rate_29_97)

# Returns: '01:20:03;14'
tc_utils.GetTimeStr(4803.470, tc_utils.SmpteTimecodeDrop, rate=tc_utils.Rate_29_97)

# Returns: '01:20:03:14'
tc_utils.GetTimeStr(4803.470, tc_utils.SmpteTimecodeNonDrop, rate=tc_utils.Rate_30) 

```

**Test**

```bash
cdp py
pytest -s ./tests/test_tc_utils.py
```


## Golang

Dervied from the original code present in https://github.com/spiretechnology/go-timecode

```bash
cd go
go test -v ./timecode/ -run TestTcConversion
```

## Javascript

Derived from the original code present in https://github.com/spiretechnology/js-timecode

```bash
npm i
npm run test
```

## JS Usage
```bash
npm start

import  * as tcUtils from './dist/index';

# Returns: "smpte_timecode_non_drop"
tcUtils.getTimecodeType("01:02:03:04")

# Returns: 4803.46699
tcUtils.parseTimeStr("01:20:03:14", tcUtils.Rate_30)

# Returns: 4803.465
tcUtils.parseTimeStr("01:20:03;14", tcUtils.Rate_29_97)

# Returns: '01:20:03;14'
tcUtils.getTimeStr(4803.470, tcUtils.smpteTimecodeDrop, tcUtils.Rate_29_97)

# Returns: '01:20:03:14'
tcUtils.getTimeStr(4803.470, tcUtils.smpteTimecodeNonDrop, tcUtils.Rate_30) 

```

## Testing

The above tests test the following:

- Generate time codes for labeling every fram in a span of 24 hours
- Convert the timecodes to float time stamp
- Convert the float time stamp back to timecode
- Compare the original timecode with the converted timecode


## Reference

1. https://support.telestream.net/s/article/Time-code-for-23-976-frames-p
2. http://www.andrewduncan.net/timecodes/ 