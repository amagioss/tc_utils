const { SmpteTimecodeNonDrop, SmpteTimecodeDrop, floatSeconds, NormalTimestamp, Rate_24, Rate_29_97, Rate_59_94, Rate_23_976, Rate_30, ParseTimeStr, GetTimeStr, GetTimecodeType } = require('../src/index');

describe('Test Timecode Type', () => {
  const testCases = [
      ["00:08:42:03", SmpteTimecodeNonDrop],
      ["00:14:47:18", SmpteTimecodeNonDrop],
      ["00:22:23;16", SmpteTimecodeDrop],
      ["00:29:16;18", SmpteTimecodeDrop],
      ["01:03:19.345", NormalTimestamp],
      ["01:09:48.25", NormalTimestamp],
      ["3456.789", floatSeconds],
      ["876.123", floatSeconds],
      ["5.678", floatSeconds]
  ];

  testCases.forEach(([input, expected]) => {
      test(`should return ${expected} for input ${input}`, () => {
          expect(GetTimecodeType(input)).toBe(expected);
      });
  });
});

describe('Non-Drop Frame Timecode Tests', () => {
    const testCases = [
        ["00:08:42:03", Rate_29_97, 522.6221],
        ["00:14:47:18", Rate_29_97, 888.4876],
        ["00:22:23:16", Rate_29_97, 1344.8768666666667],
        ["00:29:16:18", Rate_29_97, 1758.3566],
        ["00:37:28:23", Rate_29_97, 2251.0154333333335],
        ["00:44:17:05", Rate_29_97, 2659.8238333333334],
        ["00:50:42:05", Rate_29_97, 3045.208833333333],
        ["00:57:34:19", Rate_29_97, 3458.0879666666665],
        ["01:03:19:21", Rate_29_97, 3803.4997],
        ["01:09:48:16", Rate_29_97, 4192.721866666667],
        ["01:17:41:10", Rate_29_97, 4665.9946666666665],
        ["01:31:32:15", Rate_29_97, 5497.9925],
        ["01:39:23:23", Rate_30, 5963.7666],
        ["01:47:18:23", Rate_23_976, 6445.397291666667],
        ["01:47:18:23", Rate_24, 6438.958333333333],
        ["01:17:41:52", Rate_59_94, 4666.528533333333],
    ];

    testCases.forEach(([input, rate, expected]) => {
        test(`should correctly derive timestamp for ${input} at rate ${rate}`, () => {
            const derived_ts = ParseTimeStr(input, rate);
            
            // Compare derived timestamp with expected
            const tolerance = 0.001;
            if (Math.abs(derived_ts - expected) > tolerance) {
                console.error(`Mismatch between actual and derived ts: ${derived_ts} vs expected: ${expected}`);
                console.error(`Input: ${input}`);
                throw new Error("Timestamp mismatch");
            }

            const ndf_timecode = GetTimeStr(derived_ts, SmpteTimecodeNonDrop, rate);
            expect(ndf_timecode).toBe(input);
        });
    });
});


describe('testing timecode', () => {
  const testCases = [
    { framerate: Rate_29_97, sep: ';', timestampFormat: SmpteTimecodeDrop },
    { framerate: Rate_59_94, sep: ';', timestampFormat: SmpteTimecodeDrop },
    { framerate: Rate_23_976, sep: ':', timestampFormat: SmpteTimecodeNonDrop },
    { framerate: Rate_30, sep: ':', timestampFormat: SmpteTimecodeNonDrop },
    { framerate: Rate_29_97, sep: '.', timestampFormat: NormalTimestamp}
  ];
  testCases.forEach(({ framerate, sep, timestampFormat }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominalFr = framerate.nominal;
      let frameNum = 0;
      let frameNumInNominal = 0;
      for(let i = 0; i <= nominalFr * 60 * 60 * 24 + 1 ; i++) {
        let seconds, hh, mm, ss, nnn, timecodeStr, ff;
        if(timestampFormat == NormalTimestamp) {
          seconds = (frameNum * framerate.den) / framerate.num
          hh = parseInt((seconds / 3600).toString())
          mm = (parseInt((seconds / 60).toString())) % 60
          ss = parseInt(seconds.toString()) % 60
          nnn = parseInt((((frameNum * framerate.den) / framerate.num) * 1000).toString()) % 1000
          timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(nnn).padStart(3, '0')}`;
        } else {
          hh = parseInt((frameNumInNominal/(3600 * nominalFr)).toString())
          mm = parseInt((frameNumInNominal / (60 * nominalFr)).toString()) % 60
          ss = parseInt(((frameNumInNominal/nominalFr) % 60).toString())
          ff = frameNumInNominal % nominalFr
          timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;
        }
        const derivedTs = ParseTimeStr(timecodeStr, framerate);
        const derivedTc = GetTimeStr(derivedTs, timestampFormat, framerate);

        if (timecodeStr != derivedTc) {
          console.log("Mismatch between actual and derived timecode:", timecodeStr, derivedTc);
          console.log("frame_num_in_nominal:", frameNumInNominal);
          console.log("frame_num:", frameNum);
          console.log("derived_ts:", derivedTc);
          throw new Error("Timecode mismatch");
        }
        
        const actualTs = parseFloat((frameNum * framerate.den).toString()) / framerate.num;
        if(Math.abs(derivedTs - actualTs) > 0.02) {
          console.error("Mismatch between actual and derived ts:", actualTs, derivedTs);
          console.error("frame_num_in_nominal:", frameNumInNominal)
          console.error("frame_num:", frameNum)
          throw new Error("Timecode mismatch");
        }

        frameNum += 1;
        if ((frameNumInNominal + 1) % (nominalFr * 60) === 0 && ((frameNumInNominal + 1) % (nominalFr * 60 * 10)) !== 0) {
          frameNumInNominal += (framerate.drop + 1);
        } else {
          frameNumInNominal += 1;
        }
      }
    });
  })
})
