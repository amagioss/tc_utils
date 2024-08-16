
from .parse import ParseTimecode, FromSeconds, timecodeRegex, normaTimeRegex
from .timecode import Rate_23_976, Rate_24, Rate_25, Rate_29_97, Rate_30, Rate_50, Rate_59_94, Rate_60
import re


FloatSeconds = "float_seconds"
NormalTimestamp = "normal_timestamp"
SmpteTimecodeNonDrop = "smpte_timecode_nondrop"
SmpteTimecodeDrop = "smpte_timecode_drop"


def GetTimecodeType(time_str: str) -> str:
    if normaTimeRegex.match(time_str):
        return NormalTimestamp
    
    timecode_match = timecodeRegex.match(time_str)
    if timecode_match and timecode_match.group(4) == ':':
        return SmpteTimecodeNonDrop
    elif timecode_match and timecode_match.group(4) == ';':
        return SmpteTimecodeDrop
    
    # check if the string is a float value
    try:
        float(time_str)
        return FloatSeconds
    except:
        pass
    raise ValueError("Invalid time format")

def ParseTimeStr(time_str, rate=None) -> float:
    if normaTimeRegex.match(time_str):
        separated_tc = re.split("[:.]", time_str)
        tc_in_seconds = int(separated_tc[0]) * 3600 + \
                        int(separated_tc[1]) * 60 + \
                        int(separated_tc[2]) + \
                        (int(separated_tc[3]) / 1000) # rounding to the nearest millisecond
        return tc_in_seconds
    elif timecodeRegex.match(time_str):
        if rate is None:
            raise ValueError("Rate must be provided for timecode")
        return ParseTimecode(time_str, rate).Seconds()


def GetTimeStr(time_in_seconds: float, time_format, rate=None) -> str:
    """
    time_format: NormalTimestamp or SmpteTimecode
    """
    if time_format == NormalTimestamp:
        hh = int(time_in_seconds) // 3600
        mm = (int(time_in_seconds) // 60) % 60
        ss = int(time_in_seconds) % 60
        nnn = int(round(time_in_seconds - int(time_in_seconds), 3) * 1000)
        return f"{hh:02d}:{mm:02d}:{ss:02d}.{nnn:03d}"
    elif time_format == SmpteTimecodeDrop or time_format == SmpteTimecodeNonDrop:
        if time_format == SmpteTimecodeDrop:
            if rate != Rate_29_97 and rate != Rate_59_94:
                raise ValueError("Drop frame timecode is only supported for 29.97 and 59.94 fps")
        if rate is None:
            raise ValueError("Rate must be provided for timecode")
        return FromSeconds(time_in_seconds, rate, time_format).String()
    else:
        raise ValueError("Invalid format")

    
