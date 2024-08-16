package timecode_test

import (
	"fmt"
	"math"
	"testing"

	"github.com/orgs/amagioss/tc_utils/go/timecode"
	"github.com/stretchr/testify/require"
)

func TestTimecode_DFFormatAndParse(t *testing.T) {
	t.Run("parse DF timecode to frame count", func(t *testing.T) {
		require.Equal(t, timecode.MustParse("00:00:00;00", timecode.Rate_59_94).Frame(), int64(0))
		require.Equal(t, timecode.MustParse("00:00:01;00", timecode.Rate_59_94).Frame(), int64(60))
		require.Equal(t, timecode.MustParse("00:01:00;04", timecode.Rate_59_94).Frame(), int64(60*60))
	})
	t.Run("format frame count to timecode string", func(t *testing.T) {
		require.Equal(t, "00:00:00;00", timecode.FromFrame(0, timecode.Rate_59_94, true).String())
		require.Equal(t, "00:00:01;00", timecode.FromFrame(60, timecode.Rate_59_94, true).String())
		require.Equal(t, "00:01:00;04", timecode.FromFrame(60*60, timecode.Rate_59_94, true).String())
	})
	t.Run("parse and format timecodes without change", func(t *testing.T) {
		require.Equal(t, "00:00:00;00", timecode.MustParse("00:00:00;00", timecode.Rate_59_94).String())
		require.Equal(t, "00:00:01;00", timecode.MustParse("00:00:01;00", timecode.Rate_59_94).String())
		require.Equal(t, "00:00:10;00", timecode.MustParse("00:00:10;00", timecode.Rate_59_94).String())
		require.Equal(t, "00:01:00;04", timecode.MustParse("00:01:00;04", timecode.Rate_59_94).String())
		require.Equal(t, "14:55:41;22", timecode.MustParse("14:55:41;22", timecode.Rate_59_94).String())
		require.Equal(t, "14:00:41;22", timecode.MustParse("14:00:41;22", timecode.Rate_59_94).String())
		require.Equal(t, "10:55:41;00", timecode.MustParse("10:55:41;00", timecode.Rate_59_94).String())
		require.Equal(t, "14:55:41;22", timecode.MustParse("14:55:41;22", timecode.Rate_59_94).String())
		require.Equal(t, "14:55:04;22", timecode.MustParse("14:55:04;22", timecode.Rate_59_94).String())
		require.Equal(t, "13:15:00;40", timecode.MustParse("13:15:00;40", timecode.Rate_59_94).String())
	})
}

func TestTimecode_DFFrameIncrement(t *testing.T) {
	t.Run("increment frame", func(t *testing.T) {
		require.Equal(t, "14:55:41;23", timecode.MustParse("14:55:41;22", timecode.Rate_59_94).AddFrames(1).String())
		require.Equal(t, "14:57:00;04", timecode.MustParse("14:56:59;59", timecode.Rate_59_94).AddFrames(1).String())
	})
}

func TestTimecode_FrameToString_DF(t *testing.T) {
	cases := map[int64]string{
		2878: "00:01:59;22",
	}
	for f, tcode := range cases {
		tc := timecode.FromFrame(f, timecode.Rate_23_976, true)
		if str := tc.String(); str != tcode {
			t.Errorf("Frame %d should be equivalent to timecode %s. Got %s\n", f, tcode, str)
		} else {
			t.Logf("Success, frame %d equals timecode %s\n", f, tcode)
		}
	}
}

func TestTimecode_Identity_DF(t *testing.T) {
	cases := []string{
		"00:02:00;02",
		"00:00:00;00",
		"00:00:59;23",
		"00:01:00;02",
		"00:03:59;23",
		"00:04:00;02",
		"00:01:59;23",
		"00:09:59;23",
		"00:10:00;00",
	}
	for _, tcode := range cases {
		tc, _ := timecode.Parse(tcode, timecode.Rate_23_976)
		if str := tc.String(); str != tcode {
			t.Errorf("Timecode %s became %s during parsing and printing\n", tcode, str)
		} else {
			t.Logf("Success, identity valid for %s\n", tcode)
		}
	}
}

func TestTimecode_AddOne_DF(t *testing.T) {
	sequences := map[string]string{
		"00:00:59;29": "00:01:00;02",
		"00:03:59;29": "00:04:00;02",
		"00:01:59;29": "00:02:00;02",
		"00:09:59;29": "00:10:00;00",
	}
	for fromTC, toTC := range sequences {
		tc, _ := timecode.Parse(fromTC, timecode.Rate_29_97)
		next := tc.AddFrames(1)
		if str := next.String(); str != toTC {
			t.Errorf("Expected %s => %s, got %s\n", fromTC, toTC, str)
		} else {
			t.Logf("Success, got %s => %s\n", fromTC, toTC)
		}
	}
}

// TestTimecodeSequenceNDF jumps to a starting point and then seeks through the frames 1 by 1 to make sure
// the generated timecodes match what the result would be if we brute forced. Brute forcing is much slower
// if we're adding multiple frames, but adding just 1 frame allows us to put it up head-to-head against
// our timecode implementation to ensure correctness.
func TestTimecodeSequenceNDF(t *testing.T) {
	startTimecodes := map[string]int{
		"00:00:00:00": 100000,
		"03:59:59:00": 100000,
	}
	for startTimecodeStr, iterations := range startTimecodes {
		prevTc, _ := timecode.Parse(startTimecodeStr, timecode.Rate_24)
		prevComp := prevTc.Components()

		// Run through all the iterations for this sample
		for i := 0; i < iterations; i++ {
			tc := prevTc.Add(timecode.Frame(1))
			comp := tc.Components()
			expectedComp := bruteForceAdd1(prevComp, timecode.Rate_24)
			if !comp.Equals(expectedComp) {
				t.Errorf("Add 1 frame, skipped from %s to %s\n", prevTc.String(), tc.String())
			}
			prevTc = tc
			prevComp = comp
		}
	}
}

func bruteForceAdd1(c timecode.Components, rate timecode.Rate) timecode.Components {
	c.Frames++
	if c.Frames >= int64(rate.Nominal) {
		c.Frames -= int64(rate.Nominal)
		c.Seconds++
		if c.Seconds >= 60 {
			c.Seconds -= 60
			c.Minutes++
			if c.Minutes >= 60 {
				c.Minutes -= 60
				c.Hours++
			}
		}
	}
	return c
}

func bruteForceAdd1_DF(c timecode.Components, rate timecode.Rate) timecode.Components {
	c = bruteForceAdd1(c, rate)
	if (c.Minutes%10 > 0) && (c.Seconds == 0) && (c.Frames < int64(rate.Drop)) {
		c.Frames = int64(rate.Drop)
	}
	return c
}

// TestTimecodeSequenceDF jumps to a starting point and then seeks through the frames 1 by 1 to make sure
// the generated timecodes match what the result would be if we brute forced. Brute forcing is much slower
// if we're adding multiple frames, but adding just 1 frame allows us to put it up head-to-head against
// our timecode implementation to ensure correctness.
func TestTimecodeSequenceDF(t *testing.T) {
	startTimecodes := map[string]int{
		"00:00:00;00": 100000,
		"03:59:59;00": 100000,
		"01:05:59;23": 100000,
	}
	for startTimecodeStr, iterations := range startTimecodes {
		prevTc, _ := timecode.Parse(startTimecodeStr, timecode.Rate_23_976)
		prevComp := prevTc.Components()

		// Run through all the iterations for this sample
		for i := 0; i < iterations; i++ {
			tc := prevTc.Add(timecode.Frame(1))
			comp := tc.Components()
			expectedComp := bruteForceAdd1_DF(prevComp, timecode.Rate_23_976)
			if !comp.Equals(expectedComp) {
				t.Errorf("Add 1 frame, skipped from %s to %s\n", prevTc.String(), tc.String())
			}
			prevTc = tc
			prevComp = comp
		}
	}
}

func TestTcType(t *testing.T) {
	tests := map[string]struct {
		TimecodeStr  string
		ExpectedType timecode.TimeFormat
	}{
		"test_1": {TimecodeStr: "00:08:42:03", ExpectedType: timecode.SmpteTimecodeNonDrop},
		"test_2": {TimecodeStr: "00:14:47:18", ExpectedType: timecode.SmpteTimecodeNonDrop},
		"test_3": {TimecodeStr: "00:22:23;16", ExpectedType: timecode.SmpteTimecodeDrop},
		"test_4": {TimecodeStr: "00:29:16;18", ExpectedType: timecode.SmpteTimecodeDrop},
		"test_5": {TimecodeStr: "01:03:19.345", ExpectedType: timecode.NormalTimestamp},
		"test_6": {TimecodeStr: "01:09:48.25", ExpectedType: timecode.NormalTimestamp},
		"test_7": {TimecodeStr: "3456.789", ExpectedType: timecode.FloatSeconds},
		"test_8": {TimecodeStr: "876.123", ExpectedType: timecode.FloatSeconds},
		"test_9": {TimecodeStr: "5.678", ExpectedType: timecode.FloatSeconds},
	}
	for name, test := range tests {
		t.Run(name, func(t *testing.T) {
			tcType := timecode.GetTimecodeType(test.TimecodeStr)
			if tcType != test.ExpectedType {
				t.Errorf("Expected %s, got %s\n", test.ExpectedType, tcType)
			}
		})
	}
}

func TestNDFToTc(t *testing.T) {
	tests := map[string]struct {
		TimecodeStr string
		FrameRate   timecode.Rate
		ExpectedTc  float64
	}{
		"test_1":  {TimecodeStr: "00:08:42:03", FrameRate: timecode.Rate_29_97, ExpectedTc: 522.6221}, // 522.6221 = ((8*60*30+42*30+3)*1001/30000)
		"test_2":  {TimecodeStr: "00:14:47:18", FrameRate: timecode.Rate_29_97, ExpectedTc: 888.4876},
		"test_3":  {TimecodeStr: "00:22:23:16", FrameRate: timecode.Rate_29_97, ExpectedTc: 1344.8768666666667},
		"test_4":  {TimecodeStr: "00:29:16:18", FrameRate: timecode.Rate_29_97, ExpectedTc: 1758.3566},
		"test_5":  {TimecodeStr: "00:37:28:23", FrameRate: timecode.Rate_29_97, ExpectedTc: 2251.0154333333335},
		"test_6":  {TimecodeStr: "00:44:17:05", FrameRate: timecode.Rate_29_97, ExpectedTc: 2659.8238333333334},
		"test_7":  {TimecodeStr: "00:50:42:05", FrameRate: timecode.Rate_29_97, ExpectedTc: 3045.208833333333},
		"test_8":  {TimecodeStr: "00:57:34:19", FrameRate: timecode.Rate_29_97, ExpectedTc: 3458.0879666666665},
		"test_9":  {TimecodeStr: "01:03:19:21", FrameRate: timecode.Rate_29_97, ExpectedTc: 3803.4997},
		"test_10": {TimecodeStr: "01:09:48:16", FrameRate: timecode.Rate_29_97, ExpectedTc: 4192.721866666667},
		"test_11": {TimecodeStr: "01:17:41:10", FrameRate: timecode.Rate_29_97, ExpectedTc: 4665.9946666666665},
		"test_12": {TimecodeStr: "01:31:32:15", FrameRate: timecode.Rate_29_97, ExpectedTc: 5497.9925},
		"test_13": {TimecodeStr: "01:39:23:23", FrameRate: timecode.Rate_30, ExpectedTc: 5963.7666},
		"test_14": {TimecodeStr: "01:47:18:23", FrameRate: timecode.Rate_23_976, ExpectedTc: 6445.397291666667}, //6445.397291666667 = (3600*24+47*60*24+18*24+23)*1001/24000
		"test_15": {TimecodeStr: "01:47:18:23", FrameRate: timecode.Rate_24, ExpectedTc: 6438.958333333333},     //6438.958333333333 = (3600*24+47*60*24+18*24+23)/24
		"test_16": {TimecodeStr: "01:17:41:52", FrameRate: timecode.Rate_59_94, ExpectedTc: 4666.528533333333},  //4666.528533333333 = (3600*60+17*60*60+41*60+52)*1001/60000
	}

	for name, test := range tests {
		t.Run(name, func(t *testing.T) {
			tc, _ := timecode.Parse(test.TimecodeStr, test.FrameRate)
			tc_seconds := tc.Seconds()
			if math.Abs(tc_seconds-test.ExpectedTc) > 0.001 {
				t.Errorf("Expected %f, got %f\n", test.ExpectedTc, tc_seconds)
			}
			ndf_timecode, _ := timecode.GetTimeStr(tc_seconds, timecode.SmpteTimecodeNonDrop, test.FrameRate)
			if ndf_timecode != test.TimecodeStr {
				t.Errorf("Expected %s, got %s\n", test.TimecodeStr, ndf_timecode)
			}
		})
	}

}

func TestTcConversion(t *testing.T) {
	// 29.97

	tests := map[string]struct {
		FrameRate timecode.Rate
		Sep       string
		TcFormat  timecode.TimeFormat
	}{
		"test_29_97":   {FrameRate: timecode.Rate_29_97, Sep: ";", TcFormat: timecode.SmpteTimecodeDrop},
		"test_59_94":   {FrameRate: timecode.Rate_59_94, Sep: ";", TcFormat: timecode.SmpteTimecodeDrop},
		"test_30":      {FrameRate: timecode.Rate_30, Sep: ":", TcFormat: timecode.SmpteTimecodeNonDrop},
		"test_23_976":  {FrameRate: timecode.Rate_23_976, Sep: ":", TcFormat: timecode.SmpteTimecodeNonDrop},
		"test_29_97_2": {FrameRate: timecode.Rate_29_97, Sep: ".", TcFormat: timecode.NormalTimestamp},
	}

	for name, test := range tests {
		t.Run(name, func(t *testing.T) {
			var timecode_str string
			nominal_fr := test.FrameRate.Nominal
			frame_num_in_nominal := 0
			frame_num := 0

			for i := 0; i < nominal_fr*60*60*24+1; i++ {
				if test.TcFormat == timecode.NormalTimestamp {
					seconds := float64(frame_num) * float64(test.FrameRate.Den) / float64(test.FrameRate.Num)

					hh := int(seconds) / 3600
					mm := (int(seconds) / 60) % 60
					ss := int(seconds) % 60
					nnn := int(float64(frame_num*test.FrameRate.Den)/float64(test.FrameRate.Num)*1000.) % 1000

					timecode_str = fmt.Sprintf("%02d:%02d:%02d%s%03d", hh, mm, ss, test.Sep, nnn)
				} else {
					hh := int(frame_num_in_nominal / (3600 * nominal_fr))
					mm := int((frame_num_in_nominal / (60 * nominal_fr)) % 60)
					ss := int(((frame_num_in_nominal / nominal_fr) % 60))
					ff := frame_num_in_nominal % nominal_fr

					timecode_str = fmt.Sprintf("%02d:%02d:%02d%s%02d", hh, mm, ss, test.Sep, ff)
				}

				derived_ts, _ := timecode.ParseTimeStr(timecode_str, test.FrameRate)

				derived_tc, _ := timecode.GetTimeStr(derived_ts, test.TcFormat, test.FrameRate)

				//fmt.Println(timecode_str, derived_tc)

				if timecode_str != derived_tc {
					t.Errorf("Mismatch between actual and derived timecode: %s %s", timecode_str, derived_tc)
					t.Errorf("frame_num_in_nominal: %d", frame_num_in_nominal)
					t.Errorf("frame_num: %d", frame_num)
					fmt.Println(timecode_str, derived_ts, derived_tc)
				}

				actual_ts := float64((frame_num)*test.FrameRate.Den) / float64(test.FrameRate.Num)

				if (derived_ts - actual_ts) > 0.02 {
					t.Errorf("Mismatch between actual and derived ts: %f %f", actual_ts, derived_ts)
					t.Errorf("frame_num_in_nominal: %d", frame_num_in_nominal)
					t.Errorf("frame_num: %d", frame_num)
				}

				frame_num += 1

				if (frame_num_in_nominal+1)%(nominal_fr*60) == 0 && ((frame_num_in_nominal+1)%(nominal_fr*60*10)) != 0 {
					frame_num_in_nominal += (test.FrameRate.Drop + 1)
				} else {
					frame_num_in_nominal += 1
				}
			}

		})
	}
}

func TestFrame(t *testing.T) {
	frame_num := 3598

	tc := timecode.FromFrame(int64(frame_num), timecode.Rate_29_97, true)
	fmt.Println(tc.String())
}
