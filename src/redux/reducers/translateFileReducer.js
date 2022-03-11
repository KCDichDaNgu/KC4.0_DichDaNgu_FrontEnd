import {
	TRANSLATEFILE_DOCUMENT_SUCCESS,
	TRANSLATEFILE_FAIL,
	TRANSLATEFILE,
	CHANGE_FILE,
	CHANGE_FILE_DOCUMENT,
	CHANGE_OUTPUT,
	CHANGE_OUTPUT_DOCUMENT,
	DETECTLANG_FILE,
	DETECTLANG_FILE_FAIL,
	DETECTLANG_FILE_SUCCESS,
	TRANSLATE_AFTER_DETECTLANG_FILE_SUCCESS,
	GETTING_SINGLE_TRANSLATION_HISTORY_SUCCESS,
	GETTING_SINGLE_LANG_DETECTION_HISTORY_SUCCESS
} from '../constant/translateFileTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	documentFile: null,
	outputTranslationFile: null,
	outputDocumentFile: null,
	currentTranslationHistory: null,
	currentLangDetectionHistory: null,
	err: null,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case CHANGE_FILE: {
		return {
			...state,
			file: action.payload.file,
		};
	}
	case CHANGE_FILE_DOCUMENT: {
		return {
			...state,
			documentFile: action.payload.file,
		};
	}
	case TRANSLATEFILE: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case TRANSLATEFILE_DOCUMENT_SUCCESS: {
		return {
			...state,
			outputDocumentFile: action.payload.data,
			currentState: STATE.SUCCESS,
		};
	}
	case TRANSLATEFILE_FAIL: {
		return {
			...state,
			currentState: STATE.FAILURE,
			err: action.payload.err,
		};
	}
	case CHANGE_OUTPUT: {
		return {
			...state,
			outputTranslationFile: action.payload.data,
		};
	}
	case CHANGE_OUTPUT_DOCUMENT: {
		return {
			...state,
			outputDocumentFile: action.payload.data,
		};
	}
	case DETECTLANG_FILE: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case DETECTLANG_FILE_FAIL: {
		return {
			...state,
			currentState: STATE.FAILURE,
			translateCode: {
				...state.translateCode,
				// detectLang: action.payload.detectLang,
			},
			err: action.payload.err,
		};
	}
	case DETECTLANG_FILE_SUCCESS: {
		return {
			...state,
			currentState: STATE.LOADING,
			translateCode: {
				...state.translateCode,
				detectLang: action.payload.detectLang,
				sourceLang: action.payload.detectLang,
			}
		};
	}
	case TRANSLATE_AFTER_DETECTLANG_FILE_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			translateCode: {
				...state.translateCode,
				sourceLang: null,
			}
		};
	}
	case GETTING_SINGLE_TRANSLATION_HISTORY_SUCCESS: {
		return Object.assign(state, {
			currentTranslationHistory: {
				...action.payload.data.data
			},
		});
	}
	case GETTING_SINGLE_LANG_DETECTION_HISTORY_SUCCESS: {
		return Object.assign(state, {
			currentLangDetectionHistory: {
				...action.payload.data.data
			},
		});
	}
	default:
		return state;
	}
}