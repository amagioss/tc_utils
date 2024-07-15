
import tc_utils 


# def test_1():
#     frame = 3598
#     time = 3598 / 29.97

#     tc = tc_utils.FromSeconds(time, tc_utils.Rate_29_97).String()
#     print(tc)


def test_verify_29_97():
    frame_num_in_30fps = 0
    frame_num_in_29_97 = 0

    for i in range(0, 1800*60*24+1):
        hh = int(frame_num_in_30fps/(3600 * 30))
        mm = int((frame_num_in_30fps/(60 * 30)) % 60)
        ss = int(((frame_num_in_30fps/30) % 60))
        ff = frame_num_in_30fps % 30

        timecode_str = f"{hh:02d}:{mm:02d}:{ss:02d};{ff:02d}"

        drived_ts = tc_utils.ParseTimeStr(timecode_str, tc_utils.Rate_29_97)

        derived_tc = tc_utils.GetTimeStr(drived_ts, tc_utils.SmpteTimecode, rate=tc_utils.Rate_29_97)

        # print(frame_num_in_29_97, frame_num_in_30fps, timecode_str, drived_ts, derived_tc)

        if timecode_str != derived_tc:
            print("Mismatch between actual and derived timecode:", timecode_str, derived_tc)
            print("frame_num_in_30fps:", frame_num_in_30fps)
            print("frame_num_in_29_97:", frame_num_in_29_97)
            print("drived_ts:", drived_ts)
            raise


        actual_ts = float(frame_num_in_29_97)/29.97

        if abs(actual_ts - drived_ts) > 0.03:
            print("Mismatch between actual and derived ts:", actual_ts, drived_ts)

        frame_num_in_29_97 += 1

        if (frame_num_in_30fps+1) % (30*60) == 0 and ((frame_num_in_30fps+1) % (30*60*10)) != 0:
            frame_num_in_30fps += 3
        else:
            frame_num_in_30fps += 1
        