import {
	TRANSLATEFILE_SUCCESS,
	TRANSLATEFILE_FAIL,
	TRANSLATEFILE_AUDIO_SUCCESS,
	TRANSLATEFILE_AUDIO_CONVERTED,
	TRANSLATEFILE_DOCUMENT_SUCCESS,
	TRANSLATEFILE,
	CHANGE_FILE_DOCUMENT,
	CHANGE_FILE_AUDIO,
	CHANGE_OUTPUT,
	CHANGE_OUTPUT_AUDIO,
	CHANGE_OUTPUT_DOCUMENT,
	CHANGE_FILE_AUDIO_VOICE_INPUT,
	SET_TRANSLATE_SET_TIMEOUT_ID
} from '../constant/translateFileTypes';
import * as axiosHelper from '../../helpers/axiosHelper';
import { debounce } from 'lodash';


const STATUS = {
	TRANSLATING: 'translating',
	TRANSLATED: 'translated',
	CONVERTING: 'converting',
	CONVERTED: 'converted',
	CANCELLED: 'cancelled',
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

export function changeFileAudio(data) {
	return {
		type: CHANGE_FILE_AUDIO,
		payload: {
			file: data,
		}
	};
}

export function changeFileAudioVoiceInput(file, voiceInput) {
	return {
		type: CHANGE_FILE_AUDIO_VOICE_INPUT,
		payload: {
			file: file,
			voiceInput: voiceInput
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

export function changeOutputAudio(data) {
	return {
		type: CHANGE_OUTPUT_AUDIO,
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

export function translationFileAudioSuccess(data) {
	return {
		type: TRANSLATEFILE_AUDIO_SUCCESS,
		payload: {
			data,
		}
	};
}

export function translationFileAudioConverted(data) {
	return {
		type: TRANSLATEFILE_AUDIO_CONVERTED,
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

export function setTranslateSetTimeoutId(id) {
	return {
		type: SET_TRANSLATE_SET_TIMEOUT_ID,
		payload: {
			id
		}
	};
}
/**
 * @description Do BE bắt fai kiểm tra status 
 * nên sẽ gọi lại API khi nào status được dịch.
 * Đặt thời gian mỗi lần gọi lại API 
 * ! => tránh việc gọi liên tục và ko cần thiết
 */
const recursiveCheckStatus = async (translationHistoryId, taskId, time, dispatch) => {
	const getTranslationHistoryResult = await axiosHelper.getTranslateHistoryGetSingle({
		translationHistoryId,
		taskId,
	});

	if (getTranslationHistoryResult.data.status !== STATUS.TRANSLATED) {
		return new Promise((resolve, reject) => {
			let timeoutID = setTimeout(async () => {
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
			}, 1000);
			dispatch(setTranslateSetTimeoutId(timeoutID));
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
		let time = 1;
		const postTranslationResult = await axiosHelper.translateFile(body);

		const getTranslationFileResult = await recursiveCheckStatus(
			postTranslationResult.data.translationHitoryId,
			postTranslationResult.data.taskId,
			time,
			dispatch
		);
		
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

export const translateFileDocumentAsync = (body) => (dispatch) => {
	if (body.get('file') !== null) {
		dispatch(translationFileLoading());
		debouncedTranslationFile(body, dispatch);
	}
};

export const translateFileAudioAsync = (body) => (dispatch) => {
	if (body.get('file') !== null) {
		dispatch(translationFileLoading());
		debouncedTranslationFileAudio(body, dispatch);
	}
};

const recursiveCheckTranslateAudioStatus = async (translationHistoryId, taskId, time, checkStatus, dispatch) => {
	const getTranslationHistoryResult = await axiosHelper.getSpeechRecogntionHistoryGetSingle({
		translationHistoryId,
		taskId,
	});

	if (getTranslationHistoryResult.data.status == STATUS.CANCELLED) {
		dispatch(translationFileFailed('unexpected error'));
		return getTranslationHistoryResult;
	}

	if (getTranslationHistoryResult.data.status !== checkStatus && getTranslationHistoryResult.data.status !== 'translated') {
		return new Promise((resolve, reject) => {
			let timeoutID = setTimeout(async () => {
				try {
					const getTranslationHistoryResult = await recursiveCheckTranslateAudioStatus(translationHistoryId, taskId, time, checkStatus, dispatch);
					resolve(getTranslationHistoryResult);
				} catch (e) {
					reject(e);
				}
			}, 1000);

			dispatch(setTranslateSetTimeoutId(timeoutID));
		});
	} else {
		return getTranslationHistoryResult;
	}
};

/**
 * @description Nhập từ input => đợi 1 khoảng thời gian đẻ nhận text
 * ! Tránh việc gọi API ko cần thiêt và liên tục
 */
const debouncedTranslationFileAudio = debounce(async (body, dispatch) => {
	try {
		let time = 1;
		const postTranslationResult = await axiosHelper.translateFileAudio(body);

		const getConvertResult = await recursiveCheckTranslateAudioStatus(
			postTranslationResult.data.translationHitoryId,
			postTranslationResult.data.taskId,
			time,
			STATUS.TRANSLATING,
			dispatch
		);

		if (getConvertResult.message === 'Time Out') {
			dispatch(translationFileFailed(getConvertResult.message));
		} else {
			const getTranslationResult = await axiosHelper.getTranslateResultBeta(getConvertResult.data.resultUrl);

			if (getTranslationResult.status === 'translating' || getTranslationResult.status === 'translated') {
				dispatch(translationFileAudioConverted(getTranslationResult));
			} else {
				dispatch(translationFileFailed(getTranslationResult.message));
			}
		}

		const getTranslateResult = await recursiveCheckTranslateAudioStatus(
			postTranslationResult.data.translationHitoryId,
			postTranslationResult.data.taskId,
			time,
			STATUS.TRANSLATED,
			dispatch
		);

		if (getTranslateResult.message === 'Time Out') {
			dispatch(translationFileFailed(getConvertResult.message));
		} else {
			const getTranslationResult = await axiosHelper.getTranslateResultBeta(getTranslateResult.data.resultUrl);

			if (getTranslationResult.status === 'translated') {
				dispatch(translationFileAudioSuccess(getTranslationResult));
			} else {
				dispatch(translationFileFailed(getTranslationResult.message));
			}
		}
	} catch (error) {
		dispatch(translationFileFailed(error));
	}
}, 0);
