const { SmpteTimecode, Rate_29_97, Rate_59_94, Rate_23_976, Rate_30, ParseTimeStr, GetTimeStr } = require('../src/index');

describe('testing timecode', () => {
  const testCases = [
    { framerate: Rate_29_97, sep: ';' },
    { framerate: Rate_59_94, sep: ';' },
    { framerate: Rate_23_976, sep: ':' },
    { framerate: Rate_30, sep: ':' },
  ];
  testCases.forEach(({ framerate, sep }) => {
    test(`Timecode conversion at ${framerate.nominal} fps with separator '${sep}'`, () => {
      const nominalFr = framerate.nominal;
      let frameNum = 0;
      let frameNumInNominal = 0;
      for(let i = 0; i <= nominalFr * 60 * 60 * 24 + 1 ; i++) {
        const hh = parseInt((frameNumInNominal / (3600 * nominalFr)).toString());
        const mm = parseInt(((frameNumInNominal / (60 * nominalFr)) % 60).toString());
        const ss = parseInt(((frameNumInNominal / nominalFr) % 60).toString());
        const ff = frameNumInNominal % nominalFr;
        const timecodeStr = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}${sep}${String(ff).padStart(2, '0')}`;

        const derivedTs = ParseTimeStr(timecodeStr, framerate);
        const derivedTc = GetTimeStr(derivedTs, SmpteTimecode, framerate);

        if (timecodeStr !== derivedTc) {
          console.log("Mismatch between actual and derived timecode:", timecodeStr, derivedTc);
          console.log("frame_num_in_nominal:", frameNumInNominal);
          console.log("frame_num:", frameNum);
          console.log("derived_ts:", derivedTc);
          throw new Error("Timecode mismatch");
        }
        const actualTs = parseFloat((frameNum * framerate.den).toString()) / framerate.num;
        if(Math.abs(derivedTs - actualTs) > 0.02 ) {
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
