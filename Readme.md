

# TC Utils

This repo has utility packages in JS to convert between media timecodes. Timecodes
can be in one of the following formats:

- SMPTE (HH:MM:SS:FF(non-drop frame) or HH:MM:SS;FF(drop frame))
- Normal Playout time (HH:MM:SS.nnn)
- Float (seconds)

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

- Generate time codes for labeling every frame in a span of 24 hours
- Convert the timecodes to float time stamp
- Convert the float time stamp back to timecode
- Compare the original timecode with the converted timecode


## Reference

1. https://support.telestream.net/s/article/Time-code-for-23-976-frames-p
2. http://www.andrewduncan.net/timecodes/ 