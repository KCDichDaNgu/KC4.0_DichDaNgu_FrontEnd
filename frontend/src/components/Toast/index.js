
import { toast } from 'react-toastify';
import ToastSuccess from './toastError';
import React from 'react';

export const ToastError = (message) => {
	toast.error(<ToastSuccess message={message} />, {
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