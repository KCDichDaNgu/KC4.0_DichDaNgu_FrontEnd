import { SIDE_BAR_SHOW, SIDE_BAR_HIDE, CHANGE_IS_LOGIN } from '../constant/navbarTypes';

const initialState = {
	shownavbar: false,
	isLogin: false,
};

export default function(state = initialState, action) {
	switch (action.type) {
	case SIDE_BAR_SHOW: {
		return {
			...state,
			shownavbar: true,
		};
	}
	case SIDE_BAR_HIDE: {
		return {
			...state,
			shownavbar: false,
		};
	}
	case CHANGE_IS_LOGIN: {
		return {
			...state,
			isLogin: action.data
		};
	}
	default:
		return state;
	}
}
