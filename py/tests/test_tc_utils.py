
import tc_utils 
import pytest


@pytest.mark.parametrize('input, expected', [
    ("00:08:42:03", tc_utils.SmpteTimecodeNonDrop),
    ("00:14:47:18", tc_utils.SmpteTimecodeNonDrop),
    ("00:22:23;16", tc_utils.SmpteTimecodeDrop),
    ("00:29:16;18", tc_utils.SmpteTimecodeDrop),
    ("01:03:19.345", tc_utils.NormalTimestamp),
    ("01:09:48.25", tc_utils.NormalTimestamp),
    ("3456.789", tc_utils.FloatSeconds),
    ("876.123", tc_utils.FloatSeconds),
    ("5.678", tc_utils.FloatSeconds),])
def test_tc_type(input, expected):
    assert tc_utils.GetTimecodeType(input) == expected

@pytest.mark.parametrize('input, expected', [
    ("00:08:42:03", 522.6221),
    ("00:14:47:18", 888.4876),
    ("00:22:23:16", 1344.8768666666667),
    ("00:29:16:18", 1758.3566),
    ("00:37:28:23", 2251.0154333333335),
    ("00:44:17:05", 2659.8238333333334),
    ("00:50:42:05", 3045.208833333333),
    ("00:57:34:19", 3458.0879666666665),
    ("01:03:19:21", 3803.4997),
    ("01:09:48:16", 4192.721866666667),
    ("01:17:41:10", 4665.9946666666665),
    ("01:31:32:15", 5497.9925),])
def test_ndf_29_97_tc(input, expected):
    derived_ts = tc_utils.ParseTimeStr(input, tc_utils.Rate_29_97)
    if abs(derived_ts - expected) > 0.001:
        print("Mismatch between actual and derived ts:", derived_ts, expected)
        print("input:", input)
        raise
    ndf_timecode = tc_utils.GetTimeStr(derived_ts, tc_utils.SmpteTimecodeNonDrop, rate=tc_utils.Rate_29_97)
    assert ndf_timecode == input


@pytest.mark.parametrize('framerate, sep, timestamp_format', [
    (tc_utils.Rate_29_97, ';',tc_utils.SmpteTimecodeDrop),
    (tc_utils.Rate_59_94, ';',tc_utils.SmpteTimecodeDrop),
    (tc_utils.Rate_23_976, ':',tc_utils.SmpteTimecodeNonDrop),
    (tc_utils.Rate_30, ':',tc_utils.SmpteTimecodeNonDrop),
    (tc_utils.Rate_29_97, '.',tc_utils.NormalTimestamp),
])
def test_tc_conversion(framerate, sep, timestamp_format): 
    nominal_fr = framerate.nominal
    frame_num = 0
    frame_num_in_nominal = 0
    
    for i in range(0, nominal_fr*60*60*24+1):
        if timestamp_format == tc_utils.NormalTimestamp:
            seconds = (frame_num * framerate.den) / framerate.num
            hh = int(seconds) // 3600
            mm = (int(seconds) // 60) % 60
            ss = int(seconds) % 60
            nnn = int(round((frame_num * framerate.den) / framerate.num, 3) * 1000) % 1000
            timecode_str = f"{hh:02d}:{mm:02d}:{ss:02d}{sep}{nnn:03d}"
        else:
            hh = int(frame_num_in_nominal/(3600 * nominal_fr))
            mm = int((frame_num_in_nominal/(60 * nominal_fr)) % 60)
            ss = int(((frame_num_in_nominal/nominal_fr) % 60))
            ff = frame_num_in_nominal % nominal_fr
            timecode_str = f"{hh:02d}:{mm:02d}:{ss:02d}{sep}{ff:02d}"
        
        derived_ts = tc_utils.ParseTimeStr(timecode_str, framerate)

        derived_tc = tc_utils.GetTimeStr(derived_ts, timestamp_format, rate=framerate)

        if timecode_str != derived_tc:
            print("Mismatch between actual and derived timecode:", derived_ts,  timecode_str, derived_tc)
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

