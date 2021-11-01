import {
	GET_USER_LIST_SUCCESS,
	GET_USER_SUCCESS
} from '../constant/userTypes';
import * as axiosHelper from '../../helpers/axiosHelper';

export function getUserListSuccess(list, total) {
	return {
	  type: GET_USER_LIST_SUCCESS,
	  payload: {
			data: list,
			total,
		}
	};
}

export function getUserSuccess(user) {
	return {
	  type: GET_USER_SUCCESS,
	  payload: {
			data: user,
		}
	};
}

export const getCurrentUser = () => async (dispatch) => {
	try {
		const result = await axiosHelper.getMe();
		localStorage.setItem('user', JSON.stringify(result.data));
		dispatch(getUserSuccess(result.data));
	}catch(e) {
		alert(e);
	}
};

export const getUserAsync = (params) => async (dispatch) => {
	try {
		const result = await axiosHelper.getUserList(params);

		dispatch(getUserListSuccess(result.data.list, result.data.total_entries));
	}catch(e) {
		alert(e);
	}
};