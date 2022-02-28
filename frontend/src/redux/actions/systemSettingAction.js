import {
	GET_SYSTEM_SETTING_SUCCESS
} from '../constant/systemSettingTypes';
import * as axiosHelper from '../../helpers/axiosHelper';

export function getSystemSettingSuccess(system_setting) {
	return {
        type: GET_SYSTEM_SETTING_SUCCESS,
        payload: {
            data: system_setting,
		}
	};
}

export const updateSystemSettingAsync = (params) => async (dispatch) => {
	try {
		const result = await axiosHelper.getUserList(params);

		dispatch(getSystemSettingSuccess(result.data));
	}catch(e) {
		console.log(e);
	}
};

export const getSystemSettingAsync = (params) => async (dispatch) => {
	try {
		const result = await axiosHelper.getUserList(params);

		dispatch(getSystemSettingSuccess(result.data));
	}catch(e) {
		console.log(e);
	}
};