import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { Parse } from '../parse';
import {
	Rate,
	Rate_23_976,
	Rate_24,
	Rate_29_97,
	Rate_30,
	Rate_59_94,
	Rate_60,
} from '../rate';
import { Timecode } from '../timecode';

async function runTimecodesTest(
	rate: Rate,
	dropFrame: boolean,
	filename: string,
	maxFrames?: number
) {
	const fileStream = fs.createReadStream(
		path.resolve(__dirname, '../../testdata', filename)
	);
	const rl = readline.createInterface({
		input: fileStream,
		terminal: false,
	});

	let prevTimecode: Timecode | null = null;
	let frameIndex = -1;
	for await (const line of rl) {
		frameIndex++;
		if (maxFrames && frameIndex >= maxFrames) break;
		if (line.trim() === '') continue;

		// Frame index -> timecode string
		const tcFromIndex = new Timecode(frameIndex, rate, dropFrame);
		expect(tcFromIndex.toString()).toBe(line);

		// Timecode string -> frameIndex
		const tcFromStr = Parse(line, rate);
		expect(tcFromStr.frame).toBe(frameIndex);

		// Compare to the previous timecode
		if (prevTimecode != null) {
			const prevPlusOne = prevTimecode.add(1);
			expect(prevPlusOne.toString()).toBe(tcFromStr.toString());
			expect(prevPlusOne.frame).toBe(frameIndex);
		}

		prevTimecode = tcFromStr;
	}
}

describe('test all timecodes exhaustively', () => {
	test('all timecodes - 23.976', async () => {
		await runTimecodesTest(Rate_23_976, false, 'tc-all-23_976.txt', 10000);
	});
	test('all timecodes - 24', async () => {
		await runTimecodesTest(Rate_24, false, 'tc-all-24.txt', 10000);
	});
	test('all timecodes - 29.97 NDF', async () => {
		await runTimecodesTest(Rate_29_97, false, 'tc-all-30.txt', 10000);
	});
	test('all timecodes - 29.97 DF', async () => {
		await runTimecodesTest(Rate_29_97, true, 'tc-all-29_97.txt', 10000);
	});
	test('all timecodes - 30', async () => {
		await runTimecodesTest(Rate_30, false, 'tc-all-30.txt', 10000);
	});
	test('all timecodes - 59.94 NDF', async () => {
		await runTimecodesTest(Rate_59_94, false, 'tc-all-60.txt', 10000);
	});
	test('all timecodes - 59.94 DF', async () => {
		await runTimecodesTest(Rate_59_94, true, 'tc-all-59_94.txt', 10000);
	});
	test('all timecodes - 60', async () => {
		await runTimecodesTest(Rate_60, false, 'tc-all-60.txt', 10000);
	});
});
