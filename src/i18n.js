import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// the translations
// (tip move them in a JSON file and import them)
const resources = {
	vi: {
		// eslint-disable-next-line no-undef
		translation: require('./translations/vi.json'),
	}
};

i18n
	.use(initReactI18next) // passes i18n down to react-i18next
	.init({
		resources,
		lng: 'vi',
		fallbackLng: 'vi',
		debug: true,
		// nsSeparator: false,
		keySeparator: '.',
		// pluralSeparator: false,
		// contextSeparator: false,
		interpolation: {
			escapeValue: false // react already safes from xss
		}
	});

export default i18n;