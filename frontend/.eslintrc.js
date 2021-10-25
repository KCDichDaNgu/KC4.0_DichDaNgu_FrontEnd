/* eslint-disable no-undef */
module.exports = {
	'env': {
		'browser': true,
		'es2021': true
	},
	'extends': [
		'eslint:recommended',
		'plugin:react/recommended',
		'plugin:react-hooks/recommended',
		'plugin:jsx-a11y/recommended',
		'plugin:import/errors',
		'prettier',
		'plugin:react-redux/recommended',
	],
	'parserOptions': {
		'ecmaFeatures': {
			'jsx': true
		},
		'ecmaVersion': 12,
		'sourceType': 'module'
	},
	'plugins': [
		'react',
		'react-hooks',
		'jsx-a11y',
		'import',
		'react-redux',
	],
	'rules': {
		'indent': [
			'error',
			'tab'
		],
		// 'linebreak-style': [
		// 	'error',
		// 	'windows'
		// ],
		'quotes': [
			'error',
			'single'
		],
		'semi': [
			'error',
			'always'
		],
		'react-hooks/exhaustive-deps': 0,
		'no-unused-vars': 2,
		'no-console': 0,
		'react-redux/connect-prefer-named-arguments': 2,
		'react-redux/prefer-separate-component-file': 0,
		'react-redux/useSelector-prefer-selectors': 0,
	},
	'settings': {
		'react': {
			'version': 'detect', // React version. "detect" automatically picks the version you have installed.
			// You can also use `16.0`, `16.3`, etc, if you want to override the detected value.
			// default to latest and warns if missing
			// It will default to "detect" in the future
		}
	}
};
