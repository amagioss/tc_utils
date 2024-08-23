import { fromSeconds, parse } from './parse';
import { Rate, Rate_29_97, Rate_59_94 } from './rate';

export * from './parse';
export * from './rate';
export * from './timecode';

const floatSeconds = "float_seconds";
const timecodeRegex = /(\d{2}):(\d{2}):(\d{2})([;:])(\d{2})/;
const normalTimeRegex = /(\d{2}):(\d{2}):(\d{2})[.](\d{1,3})/;
const normalTimestamp = "normal_timestamp";
const smpteTimecodeNonDrop = "smpte_timecode_nondrop";
const smpteTimecodeDrop = "smpte_timecode_drop";

function getTimecodeType(timeStr: string): string {
  if(normalTimeRegex.test(timeStr)) {
    return normalTimestamp;
  }
  const timecodeMatch = timecodeRegex.exec(timeStr);
  if(timecodeMatch && timecodeMatch[4] === ':') {
    return smpteTimecodeNonDrop;
  } else if(timecodeMatch && timecodeMatch[4] === ';') {
    return smpteTimecodeDrop;
  }
  if (!isNaN(parseFloat(timeStr)) && isFinite(parseFloat(timeStr))) {
    return floatSeconds;
  }
  throw new Error("Invalid time format");;
}

function parseTimeStr(timeStr: string, rate: Rate): number {
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
  return parse(timeStr, rate).seconds();
}

function getTimeStr(timeInSeconds: number, timeFormat: string, rate: Rate) {
  if (timeFormat === normalTimestamp) {
    const hh = parseInt((timeInSeconds / 3600).toString());
    const mm = parseInt((timeInSeconds / 60).toString()) % 60;
    const ss = parseInt(timeInSeconds.toString()) % 60;
    const nnn = parseInt((parseFloat((timeInSeconds - parseInt(timeInSeconds.toString())).toFixed(3)) * 1000).toString())
    return `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}.${String(nnn).padStart(3, '0')}`;
  } else if (timeFormat === smpteTimecodeDrop || timeFormat === smpteTimecodeNonDrop) {
    if(timeFormat == smpteTimecodeDrop) {
      if(rate != Rate_29_97 && rate != Rate_59_94) {
        throw new Error("Drop frame timecode is only supported for 29.97 and 59.94 fps")
      }
    }
    if (!rate) {
      throw new Error("Rate must be provided for timecode");
    }
    return fromSeconds(timeInSeconds, rate, timeFormat).toString();
  } else {
    throw new Error("Invalid format");
  }
}

export { parseTimeStr, getTimeStr, getTimecodeType, normalTimestamp, smpteTimecodeNonDrop, smpteTimecodeDrop, floatSeconds };
