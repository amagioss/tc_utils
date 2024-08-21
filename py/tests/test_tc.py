import pytest
from tc_utils import TimecodeWrapper, Rate, GetTimeStr, GetTimecodeType, ParseTimeStr

@pytest.fixture
def setup_timecode_wrappers():
    return {
        "tc1": TimecodeWrapper(24, timecode_str="00:01:00:00"),
        "tc2": TimecodeWrapper(24, timecode_str="00:01:01:00"),
        "tc3": TimecodeWrapper(24, timecode_str="00:00:59:00"),
        "tc4": TimecodeWrapper("29.97", timecode_str="00:01:00:00", drop_frame=True),
        "tc5": TimecodeWrapper("29.97", timecode_str="00:01:01:00", drop_frame=True)
    }

def test_initialization_with_timecode_str(setup_timecode_wrappers):
    tc1 = setup_timecode_wrappers["tc1"]
    assert tc1.to_string() == "00:01:00:00"
    assert tc1.to_seconds() == 60.0

def test_initialization_with_seconds(setup_timecode_wrappers):
    tc = TimecodeWrapper(24, start_frame=60)
    assert tc.to_string() == "00:01:00:00"
    assert tc.to_seconds() == 60.0

def test_initialization_with_frames(setup_timecode_wrappers):
    tc = TimecodeWrapper(24, start_frame=60)
    assert tc.to_string() == "00:01:00:00"

def test_add_frames(setup_timecode_wrappers):
    tc1 = setup_timecode_wrappers["tc1"]
    tc1 += 60
    assert tc1.to_string() == "00:02:00:00"
    assert tc1.to_seconds() == 120.0

def test_subtract_frames(setup_timecode_wrappers):
    tc1 = setup_timecode_wrappers["tc1"]
    tc1 -= 60
    assert tc1.to_string() == "00:00:00:00"
    assert tc1.to_seconds() == 0.0

def test_equality(setup_timecode_wrappers):
    tc1 = setup_timecode_wrappers["tc1"]
    tc2 = setup_timecode_wrappers["tc2"]
    assert tc1 == tc1
    assert tc1 != tc2

def test_comparisons(setup_timecode_wrappers):
    tc1 = setup_timecode_wrappers["tc1"]
    tc2 = setup_timecode_wrappers["tc2"]
    tc3 = setup_timecode_wrappers["tc3"]

    assert tc1 < tc2
    assert tc2 > tc1
    assert tc3 < tc1
    assert tc1 > tc3
    assert tc1 <= tc2
    assert tc2 >= tc1
    assert tc3 <= tc1
    assert tc1 >= tc3

def test_timecode_type_normal_timestamp():
    assert GetTimecodeType("01:01:01.500") == "normal_timestamp"

def test_timecode_type_smpte_timecode_nondrop():
    assert GetTimecodeType("01:01:01:00") == "smpte_timecode_nondrop"

def test_timecode_type_smpte_timecode_drop():
    assert GetTimecodeType("01:01:01;00") == "smpte_timecode_drop"

def test_timecode_type_float_seconds():
    assert GetTimecodeType("3661.5") == "float_seconds"

def test_parse_time_str_normal_timestamp():
    assert ParseTimeStr("01:01:01.500") == 3661.5

def test_parse_time_str_smpte_timecode():
    tc = TimecodeWrapper(24, timecode_str="00:01:00:00")
    assert ParseTimeStr("00:01:00:00", rate=Rate.generate_rate(24)) == 60.0

def test_get_time_str_normal_timestamp():
    assert GetTimeStr(3661.5, "normal_timestamp") == "01:01:01.500"

def test_get_time_str_smpte_timecode():
    tc = TimecodeWrapper(24, timecode_str="00:01:00:00")
    assert GetTimeStr(60.0, "smpte_timecode_nondrop", rate=Rate.generate_rate(24)) == "00:01:00:00"
