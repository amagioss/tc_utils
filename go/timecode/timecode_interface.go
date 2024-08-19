package timecode

import (
	"fmt"
	"math"
	"regexp"
	"strconv"
)

type TimeFormat string

const (
	FloatSeconds         TimeFormat = "float_seconds"
	NormalTimestamp      TimeFormat = "normal_timestamp"       // hh:mm:ss.nnn
	SmpteTimecodeNonDrop TimeFormat = "smpte_timecode_nondrop" // hh:mm:ss:ff
	SmpteTimecodeDrop    TimeFormat = "smpte_timecode_drop"    // hh:mm:ss;ff
)

var floatRegx = regexp.MustCompile(`^\d+(\.\d+)?$`)
var normalTimeRegex = regexp.MustCompile(`^(\d\d):(\d\d):(\d\d)\.(\d{1,3})$`)
var smpteTimeRegex = regexp.MustCompile(`^(\d\d):(\d\d):(\d\d)([:;])(\d{2})$`)

func GetTimecodeType(timeStr string) TimeFormat {
	if floatRegx.MatchString(timeStr) {
		return FloatSeconds
	} else if normalTimeRegex.MatchString(timeStr) {
		return NormalTimestamp
	} else if smpteTimeRegex.MatchString(timeStr) {
		match := smpteTimeRegex.FindStringSubmatch(timeStr)
		if match[4] == ":" {
			return SmpteTimecodeNonDrop
		} else {
			return SmpteTimecodeDrop
		}
	} else {
		return ""
	}
}

func ParseTimeStr(timeStr string, rate Rate) (float64, error) {
	if floatRegx.MatchString(timeStr) {
		return strconv.ParseFloat(timeStr, 64)
	} else if normalTimeRegex.MatchString(timeStr) {
		match := normalTimeRegex.FindStringSubmatch(timeStr)
		hh, _ := strconv.Atoi(match[1])
		mm, _ := strconv.Atoi(match[2])
		ss, _ := strconv.Atoi(match[3])
		nnn, _ := strconv.Atoi(match[4])
		// milliseconds
		ms := (hh*3600+mm*60+ss)*1000 + nnn
		return (float64(ms) / 1000.), nil
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
		hh := int(timeInSeconds) / 3600
		mm := (int(timeInSeconds) / 60) % 60
		ss := int(timeInSeconds) % 60
		nnn := int(math.Round(timeInSeconds*1000)) % 1000 // round to nearest millisecond
		return fmt.Sprintf("%02d:%02d:%02d.%03d", hh, mm, ss, nnn), nil
	case SmpteTimecodeDrop:
		if rate != Rate_29_97 && rate != Rate_59_94 {
			return "", fmt.Errorf("drop frame timecode is only supported for 29.97 and 59.94 frame rates")
		}
		return FromSeconds(timeInSeconds, rate, timeFormat).String(), nil
	case SmpteTimecodeNonDrop:
		return FromSeconds(timeInSeconds, rate, timeFormat).String(), nil
	default:
		return "", fmt.Errorf("unsupported time format: %s", timeFormat)
	}
}
