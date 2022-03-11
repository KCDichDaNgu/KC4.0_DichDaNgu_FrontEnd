import {
	GET_SYSTEM_SETTING_SUCCESS
} from '../constant/systemSettingTypes';

export const STATE = {
	INIT: 'INIT',
	LOADING: 'LOADING',
	SUCCESS: 'SUCCESS',
	FAILURE: 'FAILURE',
};

const initialState = {
	currentState: STATE.INIT,
	systemSetting: {},
	err: null,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case GET_SYSTEM_SETTING_SUCCESS: {
		return {
			...state,
			currentState: STATE.SUCCESS,
			systemSetting: action.payload.data,
		};
	}
	default:
		return state;
	}
}
