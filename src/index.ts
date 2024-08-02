import { FromSeconds, Parse } from './parse';
import { Rate } from './rate';

export * from './parse';
export * from './rate';
export * from './timecode';

const timecodeRegex = /(\d{2}):(\d{2}):(\d{2})([;:])(\d{2})/;
const normalTimeRegex = /(\d{2}):(\d{2}):(\d{2})[.](\d{3})/;
const NormalTimestamp = "normal_timestamp";
const SmpteTimecode = "smpte_timecode";

function ParseTimeStr(timeStr: string, rate: Rate): number {
  if (normalTimeRegex.test(timeStr)) {
    const separatedTc = timeStr.split(/[:.]/);
    const tcInSeconds = parseInt(separatedTc[0], 10) * 3600 +
                        parseInt(separatedTc[1], 10) * 60 +
                        parseInt(separatedTc[2], 10) +
                        (parseInt(separatedTc[3], 10) + 500) / 1000; // rounding to the nearest millisecond
    return tcInSeconds;
  } else if (timecodeRegex.test(timeStr)) {
    if (!rate) {
      throw new Error("Rate must be provided for timecode");
    }
  }
  return Parse(timeStr, rate).Seconds();
}

function GetTimeStr(timeInSeconds: number, timeFormat: string, rate: Rate) {
  if (timeFormat === NormalTimestamp) {
    const hh = parseInt((timeInSeconds / 3600).toString());
    const mm = parseInt(((timeInSeconds / 60) % 60).toString());
    const ss = parseInt((timeInSeconds % 60).toString());
    const nnn = parseInt(((timeInSeconds - parseInt((timeInSeconds).toString())) * 1000).toString());
    return `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}.${String(nnn).padStart(3, '0')}`;
  } else if (timeFormat === SmpteTimecode) {
    if (!rate) {
      throw new Error("Rate must be provided for timecode");
    }
    return FromSeconds(timeInSeconds, rate).toString();
  } else {
    throw new Error("Invalid format");
  }
}


export { ParseTimeStr, GetTimeStr, NormalTimestamp, SmpteTimecode };
