module.exports = {
	transform: { '^.+\\.ts?$': 'ts-jest' },
	testEnvironment: 'node',
	testRegex: ['js/src/.*\\.(test|spec)?\\.(ts|tsx|js)$', 'js/tests/.*\\.(test|spec)?\\.(ts|tsx|js)$'],
	moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
};
