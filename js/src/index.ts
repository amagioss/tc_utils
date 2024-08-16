import { FromSeconds, Parse } from './parse';
import { Rate, Rate_29_97, Rate_59_94 } from './rate';

export * from './parse';
export * from './rate';
export * from './timecode';

const floatSeconds = "float_seconds";
const timecodeRegex = /(\d{2}):(\d{2}):(\d{2})([;:])(\d{2})/;
const normalTimeRegex = /(\d{2}):(\d{2}):(\d{2})[.](\d{1,3})/;
const NormalTimestamp = "normal_timestamp";
const SmpteTimecodeNonDrop = "smpte_timecode_nondrop";
const SmpteTimecodeDrop = "smpte_timecode_drop";

function GetTimecodeType(timeStr: string): string {
  if(normalTimeRegex.test(timeStr)) {
    return NormalTimestamp;
  }
  const timecodeMatch = timecodeRegex.exec(timeStr);
  if(timecodeMatch && timecodeMatch[4] === ':') {
    return SmpteTimecodeNonDrop;
  } else if(timecodeMatch && timecodeMatch[4] === ';') {
    return SmpteTimecodeDrop;
  }
  if (!isNaN(parseFloat(timeStr)) && isFinite(parseFloat(timeStr))) {
    return floatSeconds;
  }
  throw new Error("Invalid time format");;
}

function ParseTimeStr(timeStr: string, rate: Rate): number {
  if (normalTimeRegex.test(timeStr)) {
    const separatedTc = timeStr.split(/[:.]/);
    const tcInSeconds = parseInt(separatedTc[0], 10) * 3600 +
                        parseInt(separatedTc[1], 10) * 60 +
                        parseInt(separatedTc[2], 10) +
                        (parseInt(separatedTc[3], 10)) / 1000; // rounding to the nearest millisecond
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
    const mm = parseInt((timeInSeconds / 60).toString()) % 60;
    const ss = parseInt(timeInSeconds.toString()) % 60;
    const nnn = parseInt((parseFloat((timeInSeconds - parseInt(timeInSeconds.toString())).toFixed(3)) * 1000).toString())
    return `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}.${String(nnn).padStart(3, '0')}`;
  } else if (timeFormat === SmpteTimecodeDrop || timeFormat === SmpteTimecodeNonDrop) {
    if(timeFormat == SmpteTimecodeDrop) {
      if(rate != Rate_29_97 && rate != Rate_59_94) {
        throw new Error("Drop frame timecode is only supported for 29.97 and 59.94 fps")
      }
    }
    if (!rate) {
      throw new Error("Rate must be provided for timecode");
    }
    return FromSeconds(timeInSeconds, rate, timeFormat).toString();
  } else {
    throw new Error("Invalid format");
  }
}


export { ParseTimeStr, GetTimeStr, GetTimecodeType, NormalTimestamp, SmpteTimecodeNonDrop, SmpteTimecodeDrop, floatSeconds };
