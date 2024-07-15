"""
Test timecode with dropframe to timestamp conversion
"""

import pytest
from metadata_writer.transformations.ffprobe_json_to_rdf import convert_timecode_to_seconds

def timestamp_to_drop_timecode(actual_time, framerate, dropframe_per_minute):
    modulo_10th_min = int(int(actual_time) / (10*60))
    absolute_time_at_10th_mod_min = float(modulo_10th_min * 600)

    time_in_sec_since_10th_mod_min = float(actual_time) - absolute_time_at_10th_mod_min

    if int(time_in_sec_since_10th_mod_min/60) <= 5:
        v = round(float(time_in_sec_since_10th_mod_min - (1/float(framerate))), 3)
        num_min_since_10th_mod_min = int(v / 60.)
    else:
        num_min_since_10th_mod_min = int(time_in_sec_since_10th_mod_min / 60)

    actual_frames = int(round(float(time_in_sec_since_10th_mod_min * float(framerate))))

    equivalent_frames = (actual_frames + (num_min_since_10th_mod_min * dropframe_per_minute))

    total_time_in_rounded_framerate = float(absolute_time_at_10th_mod_min) + (float(equivalent_frames)/ float(round(float(framerate))))

    hh = int(total_time_in_rounded_framerate / 3600)
    mm = int((total_time_in_rounded_framerate - float(hh*3600)) / 60)
    ss = int(total_time_in_rounded_framerate - float(hh*3600 + mm*60))
    ff = int(round(float((total_time_in_rounded_framerate - float(hh*3600+mm*60+ss)) * float(round(float(framerate))))))

    return f"{hh:02d}:{mm:02d}:{ss:02d};{ff:02d}"


@pytest.mark.parametrize('framerate, dropframe_per_minute',
                         [('29.97', 2)])
def test_convert_timecode_to_seconds(framerate, dropframe_per_minute):
    frame_num_in_rounded_framerate = 0
    frame_num_in_actual_framerate = 0
    dropped_frames = 0

    for i in range(0, 60*int(round(float(framerate)))*1000+1):
        diff = (float(frame_num_in_rounded_framerate)/round(float(framerate)) - float(frame_num_in_actual_framerate)/float(framerate))
        hh = int(frame_num_in_rounded_framerate/(3600 * round(float(framerate))))
        mm = int((frame_num_in_rounded_framerate/(60 * round(float(framerate)))) % 60)
        ss = int(((frame_num_in_rounded_framerate/round(float(framerate))) % 60))
        ff = frame_num_in_rounded_framerate % round(float(framerate))
        timecode = f"{hh:02d}:{mm:02d}:{ss:02d};{ff:02d}"
        derived_ts = convert_timecode_to_seconds(timecode, framerate)

        actual_time = float(frame_num_in_actual_framerate)/float(framerate)

        derived_time_code = timestamp_to_drop_timecode(actual_time, framerate, dropframe_per_minute)

        print(actual_time, derived_ts)
        assert timecode == derived_time_code

        assert (actual_time - float(derived_ts)) <= 0.03
        
        if (frame_num_in_rounded_framerate+1) % (60*round(float(framerate))) == 0 and ((frame_num_in_rounded_framerate+1) % (60*round(float(framerate))*10)) != 0:
            frame_num_in_rounded_framerate += 3
            dropped_frames += 2
        else:
            frame_num_in_rounded_framerate += 1
        frame_num_in_actual_framerate += 1