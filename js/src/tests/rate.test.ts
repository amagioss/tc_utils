import {
	Rate,
	rateFromFraction,
	Rate_23_976,
	Rate_24,
	Rate_29_97,
	Rate_30,
	Rate_59_94,
	Rate_60,
} from '../rate';

describe('testing create framerate from fraction', () => {
	test('frame rate from fraction', () => {
		const cases: [number, number, Rate][] = [
			[24000, 1001, Rate_23_976],
			[24, 1, Rate_24],
			[30, 1, Rate_30],
			[30000, 1001, Rate_29_97],
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
			Rate_24,
			Rate_30,
			Rate_29_97,
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
});
