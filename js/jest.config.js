module.exports = {
	transform: { '^.+\\.ts?$': 'ts-jest' },
	testEnvironment: 'node',
	testRegex: ['/src/.*\\.(test|spec)?\\.(ts|tsx|js)$', '/tests/.*\\.(test|spec)?\\.(ts|tsx|js)$'],
	moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
};
