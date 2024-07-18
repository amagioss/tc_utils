package timecode

import (
	"fmt"
	"regexp"
	"strconv"
)

type TimeFormat string

const (
	NormalTimestamp TimeFormat = "normal_timestamp" // hh:mm:ss.nnn
	SmpteTimecode   TimeFormat = "smpte_timecode"   // hh:mm:ss[:;]ff
)

var floatRegx = regexp.MustCompile(`^\d+(\.\d+)?$`)
var normalTimeRegex = regexp.MustCompile(`^(\d\d):(\d\d):(\d\d)\.(\d{3})$`)
var smpteTimeRegex = regexp.MustCompile(`^(\d\d):(\d\d):(\d\d)([:;])(\d{2})$`)

func ParseTimeStr(timeStr string, rate Rate) (float64, error) {
	if floatRegx.MatchString(timeStr) {
		return strconv.ParseFloat(timeStr, 64)
	} else if normalTimeRegex.MatchString(timeStr) {
		match := normalTimeRegex.FindStringSubmatch(timeStr)
		hh, _ := strconv.Atoi(match[1])
		mm, _ := strconv.Atoi(match[2])
		ss, _ := strconv.Atoi(match[3])
		nnn, _ := strconv.Atoi(match[4])
		return float64(hh*3600 + mm*60 + ss + nnn/1000), nil
	} else if smpteTimeRegex.MatchString(timeStr) {
		match := smpteTimeRegex.FindStringSubmatch(timeStr)
		hh, _ := strconv.Atoi(match[1])
		mm, _ := strconv.Atoi(match[2])
		ss, _ := strconv.Atoi(match[3])
		ff, _ := strconv.Atoi(match[5])
		drop_frame := match[4] == ";"
		tc := FromComponents(Components{int64(hh), int64(mm), int64(ss), int64(ff)}, rate, drop_frame)
		return tc.Seconds(), nil
	} else {
		return 0, fmt.Errorf("invalid time string: %s", timeStr)
	}
}

func GetTimeStr(timeInSeconds float64, timeFormat TimeFormat, rate Rate) (string, error) {
	switch timeFormat {
	case NormalTimestamp:
		hh := int(timeInSeconds / 3600)
		mm := int((timeInSeconds - float64(hh*3600)) / 60)
		ss := int(timeInSeconds - float64(hh*3600) - float64(mm*60))
		nnn := int((timeInSeconds - float64(hh*3600) - float64(mm*60) - float64(ss)*1000))
		return fmt.Sprintf("%02d:%02d:%02d.%03d", hh, mm, ss, nnn), nil
	case SmpteTimecode:
		return FromSeconds(timeInSeconds, rate).String(), nil
	default:
		return "", fmt.Errorf("unsupported time format: %s", timeFormat)
	}
}
