import { 
	GET_HISTORY, 
	GET_HISTORY_FAIL, 
	GET_HISTORY_SUCCESS, 
	CHANGEHISTORY,
} from '../constant/historyTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	listHistory: [],
	currentHistory: null,
	total: 0,
	err: null,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case GET_HISTORY: {
		return {
			...state,
			currentState: STATE.LOADING,
		};
	}
	case GET_HISTORY_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			listHistory: action.payload.data,
			total: action.payload.total,
		};
	}
	case GET_HISTORY_FAIL: {
		return {
			...state,
			currentState: STATE.FAILURE,
			err: action.payload.err,
		};
	}
	case CHANGEHISTORY: {
		return {
			...state,
			currentHistory: action.payload.data,
		};
	}
	default:
		return state;
	}
}
