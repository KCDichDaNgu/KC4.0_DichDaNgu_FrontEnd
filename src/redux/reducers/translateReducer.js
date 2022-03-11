import { 
	TRANSLATION,
	TRANSLATION_SUCCESS,
	TRANSLATION_FAIL,
	DETECTLANG,
	DETECTLANG_FAIL,
	DETECTLANG_SUCCESS,
	TRANSLATE_AFTER_DETECTLANG_SUCCESS,
	CHANGE_SOURCE, 
	CHANGE_TARGET,
	SWAP_TRANSLATE,
	CHANGE_SOURCE_TEXT,
	CHANGE_TARGET_TEXT,
	CHANGE_DETECT_LANG,
	RESET,
	DISABLEINPUT,
	GETTING_SINGLE_TRANSLATION_HISTORY_SUCCESS,
	GETTING_SINGLE_LANG_DETECTION_HISTORY_SUCCESS
} from '../constant/translateTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	DISABLEINPUT: 'DISABLEINPUT',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	translateCode: {
		detectLang: null,
		sourceLang: null,
		targetLang: 'vi',
	},
	translateText: {
		sourceText: '',
		targetText: '',
		editTargetText: '',
	},
	currentTranslationHistory: {
		taskId: null,
		translationHistoryId: null,
	},
	isSwap: true, // True: en, zh, lo, km => vn , False: vn => en, zh, lo, km
	err: null,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case TRANSLATION: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case TRANSLATION_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			translateText: {
				...state.translateText,
				targetText: action.payload.targetText,
				editTargetText: action.payload.targetText,
			}
		};
	}
	case TRANSLATION_FAIL: {
		return {
			...state,
			currentState: STATE.FAILURE,
			err: action.payload.err,
		};
	}
	case DETECTLANG: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case DETECTLANG_SUCCESS: {
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
	case TRANSLATE_AFTER_DETECTLANG_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			translateCode: {
				...state.translateCode,
				sourceLang: null,
			},
			translateText: {
				...state.translateText,
				targetText: action.payload.targetText,
				editTargetText: action.payload.targetText,
			}
		};
	}
	case DETECTLANG_FAIL: {
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
	case CHANGE_SOURCE: {
		return {
			...state,
			translateCode: {
				...state.translateCode,
				sourceLang: action.payload.data,
			}
		};
	}
	case CHANGE_TARGET: {
		return {
			...state,
			translateCode: {
				...state.translateCode,
				targetLang: action.payload.data,
			}
		};
	}
	case SWAP_TRANSLATE: {
		return {
			...state,
			isSwap: !state.isSwap,
			translateCode: {
				sourceLang: action.payload.dataSource,
				targetLang: action.payload.dataTarget,
			}
		};
	}
	case CHANGE_SOURCE_TEXT: {
		return {
			...state,
			currentState: STATE.INIT,
			translateText: {
				...state.translateText,
				sourceText: action.payload.data,
			},
		};
	}
	case CHANGE_TARGET_TEXT: {
		return {
			...state,
			translateText: {
				...state.translateText,
				targetText: action.payload.data,
				editTargetText: action.payload.data,
			},
		};
	}
	case RESET: {
		return {
			...state,
			currentState: STATE.INIT,
			translateCode: {
				...state.translateCode,
				detectLang: null,
			},
			translateText: {
				sourceText: '',
				targetText: '',
				editTargetText: '',
			},
		};
	}
	case DISABLEINPUT: {
		return {
			...state,
			currentState: STATE.DISABLEINPUT,
		};
	}
	case CHANGE_DETECT_LANG: {
		return {
			...state,
			translateCode: {
				...state.translateCode,
				detectLang: action.payload.data,
			},
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
