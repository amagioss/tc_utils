import re
from .parse import ParseTimecode, FromSeconds, timecodeRegex, normaTimeRegex, ToFrame, FromFrame
from .timecode import Rate, Timecode

FloatSeconds = "float_seconds"
NormalTimestamp = "normal_timestamp"
SmpteTimecodeNonDrop = "smpte_timecode_nondrop"
SmpteTimecodeDrop = "smpte_timecode_drop"

Rate_24 = Rate.generate_rate(24)
Rate_25 = Rate.generate_rate(25)
Rate_30 = Rate.generate_rate(30)
Rate_29_97 = Rate.generate_rate("29.97")
Rate_50 = Rate.generate_rate(50)
Rate_59_94 = Rate.generate_rate("59.94")
Rate_60 = Rate.generate_rate(60)
Rate_23_976 = Rate.generate_rate("23.976")

def GetTimecodeType(time_str: str) -> str:
    if normaTimeRegex.match(time_str):
        return NormalTimestamp
    
    timecode_match = timecodeRegex.match(time_str)
    if timecode_match:
        if timecode_match.group(4) == ':':
            return SmpteTimecodeNonDrop
        elif timecode_match.group(4) == ';':
            return SmpteTimecodeDrop
    
    try:
        float(time_str)
        return FloatSeconds
    except ValueError:
        pass
    raise ValueError("Invalid time format")

def ParseTimeStr(time_str: str, rate: Rate = None) -> float:
    if normaTimeRegex.match(time_str):
        separated_tc = re.split("[:.]", time_str)
        tc_in_seconds = int(separated_tc[0]) * 3600 + \
                        int(separated_tc[1]) * 60 + \
                        int(separated_tc[2]) + \
                        (int(separated_tc[3]) / 1000)  # rounding to the nearest millisecond
        return tc_in_seconds
    elif timecodeRegex.match(time_str):
        if rate is None:
            raise ValueError("Rate must be provided for timecode")
        return ParseTimecode(time_str, rate).Seconds()
    else:
        raise ValueError("Invalid time format")

def GetTimeStr(time_in_seconds: float, time_format: str, rate: Rate = None) -> str:
    if time_format == NormalTimestamp:
        hh = int(time_in_seconds) // 3600
        mm = (int(time_in_seconds) // 60) % 60
        ss = int(time_in_seconds) % 60
        nnn = (round(time_in_seconds * 1000)) % 1000
        return f"{hh:02d}:{mm:02d}:{ss:02d}.{nnn:03d}"
    elif time_format in (SmpteTimecodeDrop, SmpteTimecodeNonDrop):
        if time_format == SmpteTimecodeDrop and rate not in (Rate_29_97, Rate_59_94):
            raise ValueError("Drop frame timecode is only supported for 29.97 and 59.94 fps")
        if rate is None:
            raise ValueError("Rate must be provided for timecode")
        return FromSeconds(time_in_seconds, rate, time_format).String()
    else:
        raise ValueError("Invalid format")

class TimecodeWrapper:
    """This TimecodeWrapper class provides an abstraction to ease the use of tc_utils library"""
    # TODO: add handler for seconds  
    def __init__(self, rate_str: str, timecode_str: str = None, start_frame: int = 0, start_seconds:float = 0.0,drop_frame: bool = False):
        self.rate = Rate.generate_rate(rate_str)
        self.drop_frame = drop_frame
        self.frame = self._initialize_frame(timecode_str, start_frame, start_seconds)
        self.timecode = Timecode(rate=self.rate, frame=self.frame, drop_frame=self.drop_frame)
    
    def _initialize_frame(self, timecode_str: str, start_frame: int, start_seconds: float) -> int:
        """Initializes the frame based on input parameters."""
        if timecode_str:
            timecode = ParseTimecode(timecode_str, rate=self.rate)
            return ToFrame(timecode.Components(), self.rate, self.drop_frame)
        elif start_frame != 0:
            return start_frame
        elif start_seconds != 0.0:
            timecode_format = "smpte_timecode_drop" if not isinstance(self.rate, int) else None
            timecode = FromSeconds(seconds=start_seconds, rate=self.rate, timecode_format=timecode_format)
            return timecode.Frame()
        else:
            return 0
         
    def add_frames(self, frames: int) -> None:
        self.timecode.AddFrames(frames)
    
    def subtract_frames(self, frames: int) -> None:
        self.timecode.SubtractFrames(frames)

    def to_seconds(self) -> float:
        return self.timecode.Seconds()

    def to_string(self) -> str:
        return self.timecode.String()

    def __str__(self) -> str:
        return self.to_string()

    def __eq__(self, other: 'TimecodeWrapper') -> bool:
        return self.timecode == other.timecode

    def __add__(self, frames: int) -> 'TimecodeWrapper':
        self.add_frames(frames)
        return self

    def __sub__(self, frames: int) -> 'TimecodeWrapper':
        self.subtract_frames(frames)
        return self

    def __gt__(self, other: 'TimecodeWrapper') -> bool:
        if self.rate != other.rate:
            raise ValueError("Incompatible rates")
        return self.frame > other.frame 

    def __lt__(self, other: 'TimecodeWrapper') -> bool:
        if self.rate != other.rate:
            raise ValueError("Incompatible rates")
        return self.frame < other.frame

    def __ge__(self, other: 'TimecodeWrapper') -> bool:
        if self.rate != other.rate:
            raise ValueError("Incompatible rates")
        return self.frame >= other.frame 

    def __le__(self, other: 'TimecodeWrapper') -> bool:
        if self.rate != other.rate:
            raise ValueError("Incompatible rates")
        return self.frame <= other.frame
