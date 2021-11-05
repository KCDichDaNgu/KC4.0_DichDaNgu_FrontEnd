
import { toast } from 'react-toastify';
import ToastError from './toastError';
import React from 'react';
import ToastInformLimitReached from './toastInformLimitReached';

export const toastError = (message) => {
	toast.error(<ToastError message={message} />, {
		position: 'top-right',
		autoClose: 5000,
		hideProgressBar: false,
		closeOnClick: true,
		pauseOnHover: true,
		draggable: true,
		progress: undefined,
	});
	return null;
};

export const toastInformLimitReached = (message, used, quota, type) => {
	toast.error(<ToastInformLimitReached message={message} used={used} quota={quota} type={type} />, {
		position: 'top-right',
		autoClose: 5000,
		hideProgressBar: false,
		closeOnClick: true,
		pauseOnHover: true,
		draggable: true,
		progress: undefined,
	});
	return null;
};