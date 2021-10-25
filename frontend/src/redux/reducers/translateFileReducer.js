import { 
	TRANSLATEFILE_SUCCESS,
	TRANSLATEFILE_FAIL,
	TRANSLATEFILE,
	CHANGE_FILE,
	CHANGE_OUTPUT,
} from '../constant/translateFileTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	file: null,
	outputTranslationFile: null,
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
	case TRANSLATEFILE: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case TRANSLATEFILE_SUCCESS: {
		return {
			...state,
			outputTranslationFile: action.payload.data,
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
	default:
		return state;
	}
}