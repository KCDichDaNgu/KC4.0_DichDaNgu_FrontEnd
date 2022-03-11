/* eslint-disable quotes */
// export const getHistoryLocal = () => {
// 	return localStorage.getItem('Translate');
// };

// export const deleteHistoryLocal = (id) => {
// 	const arrayHistory = localStorage.getItem('Translate') || [];
// 	const filteredItems = arrayHistory.filter(item => !id.includes(item.id));
// 	// eslint-disable-next-line quotes
// 	localStorage.setItem('Translate', filteredItems);
// };

// export const deleteAllHistoryLocal = () => {
// 	localStorage.removeItem('Translate');
// };

// export const setHistoryLocal = (data) => {
// 	const arrayHistory = getHistoryLocal || [];
// 	arrayHistory.forEach((arr) => {
// 		if (arr.id === data.id) {
// 			return null;
// 		} else {
// 			arrayHistory.push(data);
// 		}
// 	});
// 	localStorage.setItem('Translate', arrayHistory);
// };



// const arrayVocabulary = localStorage.getItem('Vocabulary') || [];

// export const checkVocabularyLocal = () => {
// 	const arr = [];
// 	if (arrayVocabulary.length == 0) {
// 		localStorage.setItem('Vocabulary', JSON.stringify(arr));
// 	}
// 	return null;
// };

// export const getVocabularyLocal = () => {
// 	return localStorage.getItem('Vocabulary');
// };

// export const deleteVocabularyLocal = (id) => {
// 	const filteredItems = arrayVocabulary.filter(item => !id.includes(item.id));
// 	localStorage.setItem('Vocabulary', filteredItems);
// };

// export const deleteAllVocabularyLocal = () => {
// 	localStorage.removeItem('Vocabulary');
// };


// export const setVocabularyLocal = (data) => {
// 	// eslint-disable-next-line quotes
// 	console.log("🚀 ~ file: localStorageHelper.js ~ line 56 ~ setVocabularyLocal ~ data", data);

// 	if (arrayVocabulary.length == 0) {
// 		arrayVocabulary.push(data);
// 	} else {
// 		arrayVocabulary.map((arr) => {
// 			if (arr.id === data.id) {
// 				return null;
// 			} else {
// 				arrayVocabulary.push(data);
// 			}
// 		});
// 	}
// 	localStorage.setItem('Vocabulary', arrayVocabulary);
// };

// eslint-disable-next-line import/no-unresolved
import { HISTORY_KEY, DICT_KEY } from '../constants/envVar';
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
		'textTranslateFrom',
		'textTranslateTo',
		'textFrom',
		'codeFrom',
		'textTo',
		'codeTo',
		'isSave'
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

const genId = () => Date.now().toString();

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
		const dictData = await localStorage.getItem(HISTORY_KEY);
		const addedId = genId();
		// console.log(addedId);
		// if there is no dict data, create new one
		if (dictData === null) {
			const addedRecord = { ...value, id: addedId };
			const blankArray = [];
			blankArray.splice(0, 0, addedRecord);
			await localStorage.setItem(HISTORY_KEY, JSON.stringify(blankArray));
			return { ...addedRecord };
		}

		const dictDataArr = JSON.parse(dictData);
		const addedRecord = { id: addedId, ...value };
		dictDataArr.splice(0, 0, addedRecord);
		if (dictDataArr.length > 10) {
			dictDataArr.pop();
		}
		await localStorage.setItem(HISTORY_KEY, JSON.stringify(dictDataArr));
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
		const dictData = await localStorage.getItem(HISTORY_KEY);
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
		const dictData = await localStorage.getItem(HISTORY_KEY);
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
		const dictData = await localStorage.getItem(HISTORY_KEY);
		if (dictData === null) {
			// console.warn('Nothing to delete');
			return null;
		}
		let dictDataArr = JSON.parse(dictData);
		dictDataArr = dictDataArr.filter((item) => item.id !== id);
		// const deletedRecord = { ...dictDataArr[deletedID] };
		// dictDataArr.splice(deletedID, 1);
		await localStorage.setItem(HISTORY_KEY, JSON.stringify(dictDataArr));
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
		await localStorage.removeItem(HISTORY_KEY);
		return true;
	} catch (error) {
		// console.warn(error);
		return null;
	}
};

/**
 * Update and then return the updated record, return null otherwise.
 *
 * @author quanganh
 * @param {number} id id to be deleted
 * @return {boolean} deleted record or null.
 */
export const updateRecord = async (id) => {
	try {
		// const dictData = await localStorage.getItem(DICT_KEY);
		// if (dictData === null) {
		// 	// console.warn('Nothing to delete');
		// 	return null;
		// }
		// let dictDataArr = JSON.parse(dictData);
		// for (let i = 1; i <= dictDataArr.length; i++) {
		// 	if (dictDataArr[i].id === id) {
		// 		return false;
		// 	}
		// }

		const hisData = await localStorage.getItem(HISTORY_KEY);
		if (hisData === null) {
			// console.warn('Nothing to delete');
			return null;
		}
		let hisDataArr = JSON.parse(hisData);

		// for (let i = 0; i <= hisDataArr.length; i++) {
		// 	if (hisDataArr[i].id === id) {
		// 		if (hisDataArr[i].isSave === true) {
		// 			return null;
		// 		}
		// 	}
		// }

		const hisDataArr1 = [];
		hisDataArr.forEach((item) => {
			if (item.id == id) {
				item.isSave = !item.isSave;
			}
			hisDataArr1.push(item);
		});

		await localStorage.setItem(HISTORY_KEY, JSON.stringify(hisDataArr1));

		return true;
	} catch (error) {
		console.warn(error);
		return null;
	}
};


/**
 * Update and then return the updated record, return null otherwise.
 *
 * @author quanganh
 * @return {boolean} deleted record or null.
 */
export const updateAllRecord = async () => {
	try {
		const dictData = await localStorage.getItem(DICT_KEY);
		if (dictData === null) {
			// console.warn('Nothing to delete');
			return null;
		}
		let dictDataArr = JSON.parse(dictData);

		// const dictDataArr1 = [];
		// await dictDataArr.forEach(async (item) => {

		// });
		for (let i = 0; i < dictDataArr.length; i += 1) {
			await updateRecord(dictDataArr[i].id);
		}


		// await localStorage.setItem(HISTORY_KEY, JSON.stringify(dictDataArr1));
		return true;
	} catch (error) {
		console.warn(error);
		return null;
	}
};