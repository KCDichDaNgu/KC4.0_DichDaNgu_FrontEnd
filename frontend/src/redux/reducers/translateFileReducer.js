import {
	TRANSLATEFILE_DOCUMENT_SUCCESS,
	TRANSLATEFILE_FAIL,
	TRANSLATEFILE,
	CHANGE_FILE,
	CHANGE_FILE_DOCUMENT,
	CHANGE_OUTPUT,
	CHANGE_OUTPUT_DOCUMENT
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
	default:
		return state;
	}
}