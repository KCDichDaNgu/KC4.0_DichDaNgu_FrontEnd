import { SIDE_BAR_SHOW, SIDE_BAR_HIDE, CHANGE_IS_LOGIN } from '../constant/navbarTypes';


export const sideBarShow = content => ({
	type: SIDE_BAR_SHOW,
	content
});

export const sideBarHide = content => ({
	type: SIDE_BAR_HIDE,
	content
});

export const changeIsLogin = data => ({
	type: CHANGE_IS_LOGIN,
	data
});
