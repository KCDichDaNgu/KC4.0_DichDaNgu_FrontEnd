import { 
	GETHISTORY, 
	GETHISTORY_FAIL, 
	GETHISTORY_SUCCESS,
	CHANGEHISTORY,
} from '../constant/historyTypes';
import * as axiosHelper from '../../helpers/axiosHelper';

/**
 * @description change current history
 */
export function changeHistory(data) {
	return {
	  type: CHANGEHISTORY,
	  payload: {
			data,
		}
	};
}

/**
 * @description get history
 */
export function getHistoryLoading() {
	return {
	  type: GETHISTORY,
	};
}

/**
 * @description Thành công và trả về kết quả dịch
 */
export function getHistorySuccess(list, total) {
	return {
	  type: GETHISTORY_SUCCESS,
	  payload: {
			data: list,
			total,
		}
	};
}

/**
 * @description Thành công và trả về err
 */
export function getHistoryFailed(err) {
	return {
	  type: GETHISTORY_FAIL,
	  payload: {
			err,
		}
	};
}

/**
 * @description Thunk function cho việc dịch từ và lấy kết quả
 */
// params: object
export const getHistoryAsync = (params) => async (dispatch) => {
	dispatch(getHistoryLoading());
	try {
		const result = await axiosHelper.getTranslateHistory(params);
		const list = await Promise.all(result.data.list.map(async (item) => {
			const result = await axiosHelper.getTranslateResult(item.resultUrl);
			return {
				id: item.id,
				...result
			};
		}));
		dispatch(getHistorySuccess(list, result.data.total_entries));
	}catch(e) {
		dispatch(getHistoryFailed(e));
	}
};