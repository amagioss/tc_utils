from tc_utils.timecode import Timecode, Rate, Components
import re

timecodeRegex = re.compile(r"(\d{2}):(\d{2}):(\d{2})([;:])(\d{2})")
normaTimeRegex = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.](\d{3})")



def FromComponents(components: Components, rate: Rate, drop_frame: bool) -> Timecode:

    if drop_frame and (components.minutes % 10 >0 ) and components.seconds == 0 and components.frames < rate.drop:
        components.frames = rate.drop


    total_minutes = components.hours * 60 + components.minutes
    total_frames = components.frames + components.seconds * rate.nominal + total_minutes * 60 * rate.nominal

    if drop_frame:
        drop_frame_incidents = total_minutes - (total_minutes // 10)
        if drop_frame_incidents > 0:
            total_frames -= (drop_frame_incidents * rate.drop)


    return Timecode(rate, total_frames, drop_frame)

def ParseTimecode(timecode: str, rate: Rate) -> Timecode: 
    match = timecodeRegex.match(timecode)
    drop_frame = match.group(4) == ';'
    if match:
        return FromComponents(Components(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(5))), rate, drop_frame)
    raise ValueError("Invalid timecode format")
    

def FromFrame(frame: int, rate: Rate, drop_frame: bool) -> Timecode:
    return Timecode(rate, frame, drop_frame)


def FromSeconds(seconds: float, rate: Rate) -> Timecode:
    frame = round(seconds * rate.num /rate.den)
    drop_frame = rate.drop != 0 

    return Timecode(rate, frame, drop_frame)