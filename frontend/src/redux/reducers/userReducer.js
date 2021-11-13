import {
	GET_USER_LIST_SUCCESS,GET_USER_SUCCESS
} from '../constant/userTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	listUser: [],
	currentUser: null,
	total: 0,
	err: null,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case GET_USER_LIST_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			listUser: action.payload.data,
		};
	}
	case GET_USER_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			user: action.payload.data,
		};
	}
	default:
		return state;
	}
}
