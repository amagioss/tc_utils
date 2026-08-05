package timecode_test

import (
	"testing"

	"github.com/amagioss/tc_utils/go/timecode"
	"github.com/stretchr/testify/require"
)

func TestRateFromFraction(t *testing.T) {
	type testCase struct {
		num, den int
		rate     timecode.Rate
	}
	cases := []testCase{
		{24000, 1001, timecode.Rate_23_976},
		{48000, 1001, timecode.Rate_47_952},
		{24, 1, timecode.Rate_24},
		{25, 1, timecode.Rate_25},
		{30, 1, timecode.Rate_30},
		{30000, 1001, timecode.Rate_29_97},
		{50, 1, timecode.Rate_50},
		{60, 1, timecode.Rate_60},
		{60000, 1001, timecode.Rate_59_94},
	}
	for _, tc := range cases {
		rate := timecode.RateFromFraction(tc.num, tc.den)
		require.Equal(t, tc.rate, rate)
	}
}

func TestRateFromFractionBuiltinRates(t *testing.T) {
	cases := []timecode.Rate{
		timecode.Rate_23_976,
		timecode.Rate_47_952,
		timecode.Rate_24,
		timecode.Rate_25,
		timecode.Rate_30,
		timecode.Rate_29_97,
		timecode.Rate_50,
		timecode.Rate_60,
		timecode.Rate_59_94,
	}
	for _, rate := range cases {
		newRate := timecode.RateFromFraction(rate.Num, rate.Den)
		require.Equal(t, rate, newRate)
	}
}

func TestParseRate(t *testing.T) {
	type testCase struct {
		str  string
		rate timecode.Rate
	}
	cases := []testCase{
		{"23.976", timecode.Rate_23_976},
		{"23.98", timecode.Rate_23_976},
		{"23.97", timecode.Rate_23_976},
		{"47.952", timecode.Rate_47_952},
		{"47.95", timecode.Rate_47_952},
		{"24", timecode.Rate_24},
		{"25", timecode.Rate_25},
		{"25.0", timecode.Rate_25},
		{"29.97", timecode.Rate_29_97},
		{"30", timecode.Rate_30},
		{"50", timecode.Rate_50},
		{"50.0", timecode.Rate_50},
		{"59.94", timecode.Rate_59_94},
		{"60", timecode.Rate_60},
	}
	for _, tc := range cases {
		rate, ok := timecode.ParseRate(tc.str)
		require.True(t, ok, "ParseRate(%q)", tc.str)
		require.Equal(t, tc.rate, rate)
	}
}
