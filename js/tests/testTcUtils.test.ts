import {Rate} from '../src/rate'
const { SmpteTimecode, Rate_29_97, Rate_59_94, Rate_23_976, Rate_30, Rate_60, Rate_24, ParseTimeStr, GetTimeStr } = require('../src/index');

describe('testing timecode', () => {
  const testCases = [
    { framerate: Rate_29_97, sep: ';' },
    { framerate: Rate_59_94, sep: ';' },
    { framerate: Rate_23_976, sep: ':' },
    { framerate: Rate_30, sep: ':' },
  ];

  //i: 0 - 60*60*24*1
  testCases.forEach(({ framerate, sep }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominal_fr = framerate.nominal;
      let frame_num = 0;
      let frame_num_in_nominal = 0;
      for(let i = 0; i <= nominal_fr * 60 * 60; i++) {
        const hh = parseInt((frame_num_in_nominal / (3600 * nominal_fr)).toString());
        const mm = parseInt(((frame_num_in_nominal / (60 * nominal_fr)) % 60).toString());
        const ss = parseInt(((frame_num_in_nominal / nominal_fr) % 60).toString());
        const ff = frame_num_in_nominal % nominal_fr;

        const timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;

        const derived_ts = ParseTimeStr(timecodeStr, framerate);

        const derived_tc = GetTimeStr(derived_ts, SmpteTimecode, framerate);

		expect(timecodeStr).toBe(derived_tc)
        const actual_ts = (frame_num * framerate.den) / framerate.num;
		expect(Math.abs(derived_ts - actual_ts)).toBeLessThanOrEqual(0.02);
      }
    });
  })

  //i: 60*60*24*1 - 60*60*24*2
  testCases.forEach(({ framerate, sep }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominal_fr = framerate.nominal;
      let frame_num = 0;
      let frame_num_in_nominal = 0;
      for(let i = nominal_fr * 60 * 60; i <= nominal_fr * 60 * 60 * 2; i++) {
        const hh = parseInt((frame_num_in_nominal / (3600 * nominal_fr)).toString());
        const mm = parseInt(((frame_num_in_nominal / (60 * nominal_fr)) % 60).toString());
        const ss = parseInt(((frame_num_in_nominal / nominal_fr) % 60).toString());
        const ff = frame_num_in_nominal % nominal_fr;

		const timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;
        const derived_ts = ParseTimeStr(timecodeStr, framerate);
        const derived_tc = GetTimeStr(derived_ts, SmpteTimecode, framerate);

		expect(timecodeStr).toBe(derived_tc)
        const actual_ts = (frame_num * framerate.den) / framerate.num;
		expect(Math.abs(derived_ts - actual_ts)).toBeLessThanOrEqual(0.02);
      }
    });
  })

  //i: 60*60*24*22 - 60*60*24*23
  testCases.forEach(({ framerate, sep }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominal_fr = framerate.nominal;
      let frame_num = 0;
      let frame_num_in_nominal = 0;
      for(let i = nominal_fr * 60 * 60 * 22; i <= nominal_fr * 60 * 60 * 23; i++) {
        const hh = parseInt((frame_num_in_nominal / (3600 * nominal_fr)).toString());
        const mm = parseInt(((frame_num_in_nominal / (60 * nominal_fr)) % 60).toString());
        const ss = parseInt(((frame_num_in_nominal / nominal_fr) % 60).toString());
        const ff = frame_num_in_nominal % nominal_fr;

		const timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;
        const derived_ts = ParseTimeStr(timecodeStr, framerate);
        const derived_tc = GetTimeStr(derived_ts, SmpteTimecode, framerate);

		expect(timecodeStr).toBe(derived_tc)
        const actual_ts = (frame_num * framerate.den) / framerate.num;
		expect(Math.abs(derived_ts - actual_ts)).toBeLessThanOrEqual(0.02);
      }
    });
  })

  //i: 60*60*24*23 - 60*60*24*24
  testCases.forEach(({ framerate, sep }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominal_fr = framerate.nominal;
      let frame_num = 0;
      let frame_num_in_nominal = 0;
      for(let i = nominal_fr * 60 * 60 * 23; i <= nominal_fr * 60 * 60 * 24; i++) {
        const hh = parseInt((frame_num_in_nominal / (3600 * nominal_fr)).toString());
        const mm = parseInt(((frame_num_in_nominal / (60 * nominal_fr)) % 60).toString());
        const ss = parseInt(((frame_num_in_nominal / nominal_fr) % 60).toString());
        const ff = frame_num_in_nominal % nominal_fr;

		const timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;
        const derived_ts = ParseTimeStr(timecodeStr, framerate);
        const derived_tc = GetTimeStr(derived_ts, SmpteTimecode, framerate);

		expect(timecodeStr).toBe(derived_tc)
        const actual_ts = (frame_num * framerate.den) / framerate.num;
		expect(Math.abs(derived_ts - actual_ts)).toBeLessThanOrEqual(0.02);
      }
    });
  })
})

describe('random timecode testing', () => {
  const dfTimecodes = ["23:59:59;29", "00:10:00;02", "01:00:00;02", "01:01:01;01", "23:59:59;29", "00:59:59;29"];
  const dfRates = [Rate_29_97, Rate_59_94]
  
  dfTimecodes.forEach((timecode: string) => {
    dfRates.forEach((rate: Rate) => {
      test(`df smpteTimecodes conversion test`, () => {
        expect(GetTimeStr(ParseTimeStr(timecode, rate), SmpteTimecode, rate)).toBe(timecode);
      });
    })
  })

  const ndfTimecodes = ["23:59:59:29", "00:10:00:02", "01:00:00:02", "01:01:01:01", "23:59:59:29", "00:59:59:29"]
  const ndfRates = [Rate_30, Rate_60]
  ndfTimecodes.forEach((timecode: string) => {
    ndfRates.forEach((rate: Rate) => {
      test(`ndf smpteTimecodes conversion test`, () => {
        expect(GetTimeStr(ParseTimeStr(timecode, rate), SmpteTimecode, rate)).toBe(timecode);
      });
    })
  })

  const timestamps = [600.066, 3600.066, 3661.034, 3599.966, 86399.966]
  const expectedThreshold = 0.02;
  const allRates = [Rate_29_97, Rate_59_94, Rate_30, Rate_60]
  timestamps.forEach((timestamp: number) => {
    allRates.forEach((rate: Rate) => {
      test(`timestamps conversion test`, () => {
        expect(Math.abs(ParseTimeStr(GetTimeStr(timestamp, SmpteTimecode, rate), rate) - timestamp)).toBeLessThanOrEqual(expectedThreshold);
      });
    })
  })
})

