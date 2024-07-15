
import re
import logging

logger = logging.getLogger()

def correction(timecode: str, framerate: str, framedrop_per_minute: int) -> float:
    drop_timecode = re.split("[:;]", timecode)
    modulo_10min_in_sec = (int(drop_timecode[0]) * 3600 + int(drop_timecode[1]) * 60) % (10 * 60)
    num_min_in_modulo = modulo_10min_in_sec / 60
    frames_at_rounded_framerate_since_10th_min = (modulo_10min_in_sec + int(drop_timecode[2])) * round(float(framerate)) + int(drop_timecode[3])
    frames_at_actual_framerate_since_10th_min = frames_at_rounded_framerate_since_10th_min - (num_min_in_modulo * framedrop_per_minute)
    correction_factor = (float(frames_at_actual_framerate_since_10th_min) / float(framerate)) - (float(frames_at_rounded_framerate_since_10th_min) / round(float(framerate)))
    return correction_factor

def convert_timecode_to_seconds(time_code: str,framerate: str) -> str:
    """
    Converts timecode to seconds
    """
    
    if re.match(r"^\d{2}:\d{2}:\d{2}:\d{2}$", time_code):
        # Format of the time_code is HH:MM:SS:FF
        separated_tc = re.split("[:]", time_code)
        tc_in_seconds = int(separated_tc[0]) * 3600 + \
                       int(separated_tc[1]) * 60 + \
                       int(separated_tc[2]) + \
                       round(int(separated_tc[3]) / float(framerate),3)
        return str(tc_in_seconds)

    elif re.match(r"^\d{2}:\d{2}:\d{2};\d{2}$", time_code):
        # Format of the time_code is HH:MM:SS;FF
        separated_tc = re.split("[:;]", time_code)
        tc_in_seconds = int(separated_tc[0]) * 3600 + \
                        int(separated_tc[1]) * 60 + \
                        int(separated_tc[2]) + \
                        (int(separated_tc[3]) / round(float(framerate)))
        if framerate == "29.97":
            tc_in_seconds += correction(time_code, framerate, 2)
        elif framerate ==  "59.94":
            tc_in_seconds += correction(time_code, framerate, 4)
        else:
            logger.warning("Media resource with Framerate: %s is not expected to have dropframe in its timecode" % framerate)
        
        return str(round(tc_in_seconds,3))
    
    elif re.match(r"^\d{2}:\d{2}:\d{2}.\d{3}$", time_code):
        # Format of the time_code is HH:MM:SS.mmm
        separated_tc = re.split("[:.]", time_code)
        tc_in_seconds = int(separated_tc[0]) * 3600 + \
                       int(separated_tc[1]) * 60 + \
                       int(separated_tc[2]) + \
                       (int(separated_tc[3]) / 1000)
        logger.info("Successfully converted timecode to seconds", extra={
            "activity": "convert_timecode_to_seconds","event": "end", "context": ctx.dict()})
        return str(tc_in_seconds)

    elif time_code.isnumeric():
        return time_code + ".0"

    elif time_code.isFloat(time_code):
        return time_code

    else:
        return ""