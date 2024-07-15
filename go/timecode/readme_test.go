package timecode_test

import (
	"testing"

	"github.com/orgs/amagioss/tc_utils/go/timecode"
	"github.com/stretchr/testify/require"
)

func TestReadmeExamples(t *testing.T) {
	t.Run("parse a timecode (drop frame)", func(t *testing.T) {
		tc := timecode.MustParse("00:01:02;23", timecode.Rate_29_97)
		require.Equal(t, "00:01:02;23", tc.String())
		require.Equal(t, int64(1881), tc.Frame())
	})
	t.Run("parse a timecode (non-drop frame)", func(t *testing.T) {
		tc := timecode.MustParse("00:01:02:23", timecode.Rate_24)
		require.Equal(t, "00:01:02:23", tc.String())
		require.Equal(t, int64(1511), tc.Frame())
	})
	t.Run("create a timecode from a frame count", func(t *testing.T) {
		tc := timecode.FromFrame(1511, timecode.Rate_24, false /* non-drop frame */)
		require.Equal(t, "00:01:02:23", tc.String())
		require.Equal(t, int64(1511), tc.Frame())
	})
	t.Run("algebra with timecodes and frames", func(t *testing.T) {
		tc := timecode.MustParse("00:01:02:23", timecode.Rate_24)
		tc = tc.Add(timecode.Frame(3))
		require.Equal(t, "00:01:03:02", tc.String())
		require.Equal(t, int64(1514), tc.Frame())
	})
}
