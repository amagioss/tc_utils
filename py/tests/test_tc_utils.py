
import tc_utils 
import pytest


# def test_1():
#     frame = 3598
#     time = 3598 / 29.97

#     tc = tc_utils.FromSeconds(time, tc_utils.Rate_29_97).String()
#     print(tc)

@pytest.mark.parametrize('framerate, sep,timestamp', [
    (tc_utils.Rate_29_97, ';',tc_utils.SmpteTimecode),
    (tc_utils.Rate_59_94, ';',tc_utils.SmpteTimecode),
    (tc_utils.Rate_23_976, ':',tc_utils.SmpteTimecode),
    (tc_utils.Rate_30, ':',tc_utils.SmpteTimecode),
    (tc_utils.Rate_59_94, '.',tc_utils.NormalTimestamp),
])
def test_tc_conversion(framerate, sep,timestamp): 
    nominal_fr = framerate.nominal
    frame_num = 0
    frame_num_in_nominal = 0
    
    for i in range(0, nominal_fr*60*60*24+1):
        hh = int(frame_num_in_nominal/(3600 * nominal_fr))
        mm = int((frame_num_in_nominal/(60 * nominal_fr)) % 60)
        ss = int(((frame_num_in_nominal/nominal_fr) % 60))
        ff = frame_num_in_nominal % nominal_fr
        nnn = int((frame_num_in_nominal % nominal_fr) * (1000 / nominal_fr))  

        timecode_str = f"{hh:02d}:{mm:02d}:{ss:02d}{sep}{ff:02d}"
        if sep == ".":
            timecode_str = f"{hh:02d}:{mm:02d}:{ss:02d}{sep}{nnn:03d}"
        
        derived_ts = tc_utils.ParseTimeStr(timecode_str, framerate)

        derived_tc = tc_utils.GetTimeStr(derived_ts, timestamp, rate=framerate)

        if timecode_str != derived_tc:
            print("Mismatch between actual and derived timecode:", timecode_str, derived_tc)
            print("frame_num_in_nominal:", frame_num_in_nominal)
            print("frame_num:", frame_num)
            print("drived_ts:", derived_ts)
            raise


        actual_ts = float((frame_num)*framerate.den)/framerate.num
        # approximate actual_ts to 3 decimal places
        # actual_ts = round(actual_ts, 3)

        if (derived_ts - actual_ts) > 0.02: # or (derived_ts > actual_ts):
            print("Mismatch between actual and derived ts:", actual_ts, derived_ts)
            print("frame_num_in_nominal:", frame_num_in_nominal)
            print("frame_num:", frame_num)

        frame_num += 1

        if (frame_num_in_nominal+1) % (nominal_fr*60) == 0 and ((frame_num_in_nominal+1) % (nominal_fr*60*10)) != 0:
            frame_num_in_nominal += (framerate.drop + 1) # 4 drop frames
        else:
            frame_num_in_nominal += 1

