const SECONDS_PER_HOUR = 3600;
const DROP_OCCURRENCES_PER_HOUR = 54;

// Rate represents a frame rate for a timecode
export interface Rate {
	nominal: number;
	drop: number;
	num: number;
	den: number;
}

export function ParseRate(str: string): Rate | null {
	switch (str) {
		case '23.976':
		case '23.98':
			return Rate_23_976;
		case '24':
			return Rate_24;
		case '29.97':
			return Rate_29_97;
		case '30':
			return Rate_30;
		case '59.94':
			return Rate_59_94;
		case '60':
			return Rate_60;
		default:
			return null;
	}
}

export function RateFromFraction(num: number, den: number): Rate {
	if (num === 24000 && den === 1001) {
		return Rate_23_976;
	} else if (num === 24 && den === 1) {
		return Rate_24;
	} else if (num === 30000 && den === 1001) {
		return Rate_29_97;
	} else if (num === 30 && den === 1) {
		return Rate_30;
	} else if (num === 60000 && den === 1001) {
		return Rate_59_94;
	} else if (num === 60 && den === 1) {
		return Rate_60;
	}

	// Calculate the nominal frame rate (number of frames in a second without drops)
	const nominal = num % den === 0 ? num / den : den - (num % den);

	// format it as a string (ie. 23.976)
	let str = (num / den).toFixed(3);
	while (str.endsWith('0')) {
		str = str.slice(0, -1);
	}
	if (str.endsWith('.')) {
		str = str.slice(0, -1);
	}

	// Calculate the number of frames to skip per drop occurrence
	const actualFramesPerHour = Math.floor((num * SECONDS_PER_HOUR) / den);
	const nominalFramesPerHour = nominal * SECONDS_PER_HOUR;
	const totalFramesDropped = nominalFramesPerHour - actualFramesPerHour;
	const framesPerDrop = Math.round(
		totalFramesDropped / DROP_OCCURRENCES_PER_HOUR
	);

	return {
		nominal,
		drop: framesPerDrop,
		num,
		den,
	};
}

export const Rate_23_976: Rate = {
	nominal: 24,
	drop: 0,
	num: 24000,
	den: 1001,
};
export const Rate_24: Rate = {
	nominal: 24,
	drop: 0,
	num: 24,
	den: 1,
};
export const Rate_30: Rate = {
	nominal: 30,
	drop: 0,
	num: 30,
	den: 1,
};
export const Rate_29_97: Rate = {
	nominal: 30,
	drop: 2,
	num: 30000,
	den: 1001,
};
export const Rate_60: Rate = {
	nominal: 60,
	drop: 0,
	num: 60,
	den: 1,
};
export const Rate_59_94: Rate = {
	nominal: 60,
	drop: 4,
	num: 60000,
	den: 1001,
};

export function GetPlaybackDurationMilliseconds(rate: Rate): number {
	return (rate.den / rate.num) * 1000;
}
