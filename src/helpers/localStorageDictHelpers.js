// eslint-disable-next-line import/no-unresolved
import { DICT_KEY } from '../constants/envVar';

// THE DICTIONARY IS AN ARRAY

/**
 * Returns true if value to be used is an object having keys: textTranslateFrom, textTranslateTo.
 *
 * @author AnLG
 * @param {object} value object to be checked
 * @return {boolean} true/false.
 */
const isValValid = (value) => {
	const allKeys = Object.keys(value);
	// console.log(allKeys);
	if (!(typeof value === 'object' && allKeys.length === 7)) {
		// console.warn(
		//   'Invalid value, need keys: textTranslateFrom, textTranslateTo',
		// );
		return false;
	}
	const requiredKeys = [
		'id',
		'textTranslateFrom',
		'textTranslateTo',
		'textFrom',
		'codeFrom',
		'textTo',
		'codeTo'
	];
	const doesContainAllKeys = requiredKeys.every((item) => allKeys.includes(item));
	if (!doesContainAllKeys) {
		// console.warn(
		//   'Invalid value, need keys: textTranslateFrom, textTranslateTo',
		// );
		return false;
	}

	return true;
};

// const genId = () => Date.now().toString();

/**
 * Create a new record for user dictionary and return the added record, return null otherwise.
 *
 * @author AnLG
 * @param {object} value object to added
 * @return {object} added record or null.
 */
export const createRecord = async (value) => {
	if (!isValValid(value)) {
		return null;
	}
	try {
		const dictData = await localStorage.getItem(DICT_KEY);
		// const addedId = genId();
		// console.log(addedId);
		// if there is no dict data, create new one
		if (dictData === null) {
			const addedRecord = { ...value };
			const blankArray = [];
			blankArray.splice(0, 0, addedRecord);
			await localStorage.setItem(DICT_KEY, JSON.stringify(blankArray));
			return { ...addedRecord };
		}

		const dictDataArr = JSON.parse(dictData);
		const addedRecord = { ...value };
		dictDataArr.splice(0, 0, addedRecord);
		if (dictDataArr.length > 20) {
			dictDataArr.pop();
		}
		await localStorage.setItem(DICT_KEY, JSON.stringify(dictDataArr));
		return { ...addedRecord };
	} catch (error) {
		// console.warn(error);
		return null;
	}
};

/**
 * Get list of words in user translation history, return blank array if there is none.
 *
 * @author AnLG
 * @return {array} list of words.
 */
export const listRecord = async () => {
	// const limit = 10;
	// const offset = 0;
	try {
		const dictData = await localStorage.getItem(DICT_KEY);
		if (dictData === null) {
			return [];
		}
		const dictDataArr = JSON.parse(dictData);
		// const slicedData = dictDataArr.slice(offset, offset + limit);
		return dictDataArr;
	} catch (error) {
		// console.warn(error);
		return [];
	}
};
/**
 * Get list of words in user translation history, return blank array if there is none.
 *
 * @author AnLG
 * @return {array} list of words.
 */
export const listRecordLimit = async () => {
	const limit = 3;
	const offset = 0;
	try {
		const dictData = await localStorage.getItem(DICT_KEY);
		if (dictData === null) {
			return [];
		}
		const dictDataArr = JSON.parse(dictData);
		const slicedData = dictDataArr.slice(offset, offset + limit);
		// console.log(`slide data ${JSON.stringify(slicedData)}`);
		return slicedData;
	} catch (error) {
		// console.warn(error);
		return [];
	}
};
/**
 * Delete and then return the deleted record, return null otherwise.
 *
 * @author AnLG
 * @param {number} id id to be deleted
 * @return {boolean} true or null.
 */
export const removeRecord = async (id) => {
	try {
		const dictData = await localStorage.getItem(DICT_KEY);
		if (dictData === null) {
			// console.warn('Nothing to delete');
			return null;
		}
		let dictDataArr = JSON.parse(dictData);
		dictDataArr = dictDataArr.filter((item) => item.id !== id);
		// const deletedRecord = { ...dictDataArr[deletedID] };
		// dictDataArr.splice(deletedID, 1);
		await localStorage.setItem(DICT_KEY, JSON.stringify(dictDataArr));
		return true;
	} catch (error) {
		// console.warn(error);
		return null;
	}
};

/**
 * Delete and then return the deleted record, return null otherwise.
 *
 * @author AnLG
 * @param {number} id id to be deleted
 * @return {object} deleted record or null.
 */
export const removeAllRecord = async () => {
	try {
		await localStorage.removeItem(DICT_KEY);
		return true;
	} catch (error) {
		// console.warn(error);
		return null;
	}
};