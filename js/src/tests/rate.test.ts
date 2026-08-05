import {
	Rate,
	parseRate,
	rateFromFraction,
	Rate_23_976,
	Rate_24,
	Rate_25,
	Rate_29_97,
	Rate_30,
	Rate_47_952,
	Rate_50,
	Rate_59_94,
	Rate_60,
} from '../rate';

describe('testing create framerate from fraction', () => {
	test('frame rate from fraction', () => {
		const cases: [number, number, Rate][] = [
			[24000, 1001, Rate_23_976],
			[48000, 1001, Rate_47_952],
			[24, 1, Rate_24],
			[25, 1, Rate_25],
			[30, 1, Rate_30],
			[30000, 1001, Rate_29_97],
			[50, 1, Rate_50],
			[60, 1, Rate_60],
			[60000, 1001, Rate_59_94],
		];
		for (const [num, den, expected] of cases) {
			const rate = rateFromFraction(num, den);
			expect(rate.num).toBe(expected.num);
			expect(rate.den).toBe(expected.den);
			expect(rate.nominal).toBe(expected.nominal);
			expect(rate.drop).toBe(expected.drop);
		}
	});
	test('frame rate from fraction for built-in rates', () => {
		const cases: Rate[] = [
			Rate_23_976,
			Rate_47_952,
			Rate_24,
			Rate_25,
			Rate_30,
			Rate_29_97,
			Rate_50,
			Rate_60,
			Rate_59_94,
		];
		for (const rate of cases) {
			const newRate = rateFromFraction(rate.num, rate.den);
			expect(newRate.num).toBe(rate.num);
			expect(newRate.den).toBe(rate.den);
			expect(newRate.nominal).toBe(rate.nominal);
			expect(newRate.drop).toBe(rate.drop);
		}
	});
	test('parse rate strings', () => {
		const cases: [string, Rate][] = [
			['23.976', Rate_23_976],
			['23.98', Rate_23_976],
			['23.97', Rate_23_976],
			['47.952', Rate_47_952],
			['47.95', Rate_47_952],
			['24', Rate_24],
			['25', Rate_25],
			['25.0', Rate_25],
			['29.97', Rate_29_97],
			['30', Rate_30],
			['50', Rate_50],
			['50.0', Rate_50],
			['59.94', Rate_59_94],
			['60', Rate_60],
		];
		for (const [str, expected] of cases) {
			expect(parseRate(str)).toBe(expected);
		}
	});
});
