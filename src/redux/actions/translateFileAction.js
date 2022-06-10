/* eslint-disable no-unused-vars */
import {
	TRANSLATEFILE_SUCCESS,
	TRANSLATEFILE_FAIL,
	TRANSLATEFILE_DOCUMENT_SUCCESS,
	TRANSLATEFILE,
	CHANGE_FILE_DOCUMENT,
	CHANGE_OUTPUT,
	CHANGE_OUTPUT_DOCUMENT,
	DETECTLANG_FILE,
	DETECTLANG_FILE_FAIL,
	DETECTLANG_FILE_SUCCESS,
	TRANSLATE_AFTER_DETECTLANG_FILE_SUCCESS,
	GETTING_SINGLE_TRANSLATION_HISTORY_SUCCESS,
	GETTING_SINGLE_LANG_DETECTION_HISTORY_SUCCESS,
} from '../constant/translateFileTypes';
import * as axiosHelper from '../../helpers/axiosHelper';
import { debounce } from 'lodash';
import { detectLangFailed, detectLangSuccess, translateAfterDetectLangSuccess } from './translateAction';

const STATUS = {
	TRANSLATING: 'translating',
	TRANSLATED: 'translated',
	CONVERTING: 'converting',
	CONVERTED: 'converted',
	CANCELLED: 'cancelled',
	DETECTING: 'detecting'
};

/**
 * @description Thay đổi giá trị
 */
export function changeFileDocument(data) {
	return {
		type: CHANGE_FILE_DOCUMENT,
		payload: {
			file: data,
		}
	};
}

/**
 * @description Thay đổi giá trị
 */
export function changeOutput(data) {
	return {
		type: CHANGE_OUTPUT,
		payload: {
			data,
		}
	};
}

export function changeOutputDocument(data) {
	return {
		type: CHANGE_OUTPUT_DOCUMENT,
		payload: {
			data,
		}
	};
}

export function translationFileLoading() {
	return {
		type: TRANSLATEFILE,
	};
}

/**
 * @description Thành công và trả về kết quả dịch
 */
export function translationFileSuccess(data) {
	return {
		type: TRANSLATEFILE_SUCCESS,
		payload: {
			data,
		}
	};
}

export function translationFileDocumentSuccess(data) {
	return {
		type: TRANSLATEFILE_DOCUMENT_SUCCESS,
		payload: {
			data,
		}
	};
}

/**
 * @description Thành công và trả về err
 */
export function translationFileFailed(err) {
	return {
		type: TRANSLATEFILE_FAIL,
		payload: {
			err,
		}
	};
}

export function detectLangFile(err) {
	return {
		type: DETECTLANG_FILE
	};
}
export function translateAfterDetectLangFileSuccess() {
	return {
		type: TRANSLATE_AFTER_DETECTLANG_FILE_SUCCESS
	};
}

export function detectLangFileFailed(err, detectLang) {
	return {
	  type: DETECTLANG_FILE_FAIL,
	  payload: {
			detectLang,
			err,
		}
	};
}

export function detectLangFileSuccess(data) {
	return {
		type: DETECTLANG_FILE_SUCCESS,
		payload: {
			detectLang: data.source_lang,
		}
	};
}

export function saveGetDetectionHistoryGetSingle(data) {
	return {
		type: GETTING_SINGLE_LANG_DETECTION_HISTORY_SUCCESS,
		payload: {
			data
		}
	};
}

export function saveGetTranslationHistoryGetSingle(data) {
	return {
		type: GETTING_SINGLE_TRANSLATION_HISTORY_SUCCESS,
		payload: {
			data
		}
	};
}

/**
 * @description Do BE bắt fai kiểm tra status 
 * nên sẽ gọi lại API khi nào status được dịch.
 * Đặt thời gian mỗi lần gọi lại API 
 * ! => tránh việc gọi liên tục và ko cần thiết
 */
const recursiveDetectionCheckStatus = async (translationHistoryId, taskId, time, dispatch) => {
	const getDetectionHistoryResult = await axiosHelper.getDetectionHistoryGetSingle({
		translationHistoryId,
		taskId,
	});

	dispatch(saveGetDetectionHistoryGetSingle(getDetectionHistoryResult))

	if (getDetectionHistoryResult.data.status === STATUS.DETECTING) {
		return new Promise((resolve, reject) => {
			setTimeout(async () => {
				try {
					const getDetectionHistoryResult = await recursiveDetectionCheckStatus(translationHistoryId, taskId, time, dispatch);
					resolve(getDetectionHistoryResult);
				} catch (e) {
					reject(e);
				}
			}, 200);
		});
	} else {
		return getDetectionHistoryResult;
	}
};

const recursiveCheckStatus = async (translationHistoryId, taskId, time, dispatch) => {
	const getTranslationHistoryResult = await axiosHelper.getTranslateHistoryGetSingle({
		translationHistoryId,
		taskId,
	});

	dispatch(saveGetTranslationHistoryGetSingle(getTranslationHistoryResult));

	if (getTranslationHistoryResult.data.status === STATUS.TRANSLATING) {
		
		return new Promise((resolve, reject) => {
			setTimeout(async () => {
				// 10 * 1000 = 10 sec
				// if (time !== 10) {
				// time += 1;
				try {
					const getTranslationHistoryResult = await recursiveCheckStatus(translationHistoryId, taskId, time, dispatch);
					resolve(getTranslationHistoryResult);
				} catch (e) {
					reject(e);
				}
				// } else {
				// reject('Time Out');
				// }
			}, 200);
		});
	} else {
		return getTranslationHistoryResult;
	}
};

/**
 * @description Nhập từ input => đợi 1 khoảng thời gian đẻ nhận text
 * ! Tránh việc gọi API ko cần thiêt và liên tục
 */
const debouncedTranslationFile = debounce(async (body, dispatch) => {
	try {
		console.log('sadasdasdasdasdsad')
		let time = 1;
		const postTranslationResult = await axiosHelper.translateFile(body);
		const getTranslationFileResult = await recursiveCheckStatus(
			postTranslationResult.data.translationHitoryId,
			postTranslationResult.data.taskId,
			time,
			dispatch
		);
		console.log('sadasdasdasdasdsad')
		if (getTranslationFileResult.message === 'Time Out') {
			dispatch(translationFileFailed(getTranslationFileResult.message));
		} else {
			const getTranslationResult = await axiosHelper.getTranslateResult(getTranslationFileResult.data.resultUrl);
			if (getTranslationResult.status === 'translated') {
				dispatch(translationFileDocumentSuccess(getTranslationResult));
			} else {
				
				dispatch(translationFileFailed(getTranslationResult.message));
			}
		}
	} catch (error) {
		dispatch(translationFileFailed(error));
	}
}, 0);

const debouncedTranslateAndDetectFile = debounce(async (body, dispatch) => {
	try {
		let time = 1;
		// Phát hiện ngôn ngữ
		const formData = new FormData();
		formData.append('file', body.sourceFile);
		const getDetectLangInstant = await axiosHelper.detectLangFile(formData);
		const getSourceLang = await recursiveDetectionCheckStatus(
			getDetectLangInstant.data.translationHitoryId, 
			getDetectLangInstant.data.taskId, 
			time,
			dispatch
		); 
	
		if(getSourceLang.message === 'Time Out'){
			dispatch(detectLangFileFailed(getSourceLang.message, 'unknown'));
			dispatch(detectLangFailed(getSourceLang.message, 'unknown'));
		} else {
			const getDetectResult = await axiosHelper.getTranslateResult(getSourceLang.data.resultUrl);
			if (getDetectResult.status === 'closed' || getDetectResult.status === 'cancelled'){
				dispatch(detectLangFileFailed(getDetectResult.message, getDetectResult.source_lang));
				dispatch(detectLangFailed(getDetectResult.message, getDetectResult.source_lang));
			} else if (getDetectResult.source_lang) {
				// Sử dụng ngôn ngữ phát hiện được và dịch
				dispatch(detectLangFileSuccess({source_lang: getDetectResult.source_lang}));
				dispatch(detectLangSuccess({source_lang: getDetectResult.source_lang}));
				formData.append('sourceLang', getDetectResult.source_lang);
				formData.append('targetLang', body.targetLang);

				const postTranslationResult = await axiosHelper.translateFile(formData);

				const getTranslationHistoryResult = await recursiveCheckStatus(
					postTranslationResult.data.translationHitoryId, 
					postTranslationResult.data.taskId, 
					time,
					dispatch
				);
				if(getTranslationHistoryResult.message === 'Time Out'){
					dispatch(detectLangFileFailed(getTranslationHistoryResult.message, 'unknown'));
					dispatch(detectLangFailed(getTranslationHistoryResult.message, 'unknown'));
				} else {
					const getTranslationResult = await axiosHelper.getTranslateResult(getTranslationHistoryResult.data.resultUrl);
					if (getTranslationResult.status === 'closed'){
						dispatch(detectLangFileFailed(getTranslationResult.message, getTranslationResult.source_lang));
						dispatch(detectLangFailed(getTranslationResult.message, getTranslationResult.source_lang));
					} else if (getTranslationResult.status === 'cancelled') {
						dispatch(detectLangFileFailed(getTranslationResult.message, getTranslationResult.source_lang));
						dispatch(detectLangFailed(getTranslationResult.message, getTranslationResult.source_lang));
					} else {
						dispatch(translationFileDocumentSuccess(getTranslationResult));
						dispatch(translateAfterDetectLangFileSuccess());
						dispatch(translateAfterDetectLangSuccess(getTranslationResult));
					}
				}
			}
		}
	} catch(error) {
		dispatch(detectLangFileFailed(error, 'unknown'));
	}
}, 0);

export const translateFileDocumentAsync = (body) => (dispatch) => {
	if (body.get('file') !== null) {
		dispatch(translationFileLoading());
		debouncedTranslationFile(body, dispatch);
	}
};

export const translationAndDetectFileAsync = (body) => (dispatch) => {
	dispatch(detectLangFile());
	debouncedTranslateAndDetectFile(body, dispatch);
};
