/* eslint-disable react/prop-types */
import { useHistory } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import React, { useEffect, useState } from 'react';
import { ACCESS_TOKEN } from '../constants/envVar';
import * as axiosHelper from '../helpers/axiosHelper';
import { changeIsLogin } from '../redux/actions/navbarAction';

const authHoc = (WrappedComponent) => {
	const FuncComponent = ({ children, ...props }) => {
		const [renderCom, setRenderCom] = useState(false);
		const dispatch = useDispatch();
		const history = useHistory();

		const redirectToLogin = () => {
			if (history.location.pathname !== '/translate') {
				history.push('/login');
			}
			else setRenderCom(true);

			dispatch(changeIsLogin(false));
			localStorage.clear();
		};

		useEffect(() => {
			const acc_token = localStorage.getItem(ACCESS_TOKEN);

			if (!acc_token) {
				redirectToLogin();
				// return;
			}

			const getMe = async () => {
				try {
					const result = await axiosHelper.getMe();

					if (!result.data.username) {
						redirectToLogin();
						// return;
					}
				}
				catch (e) {
					redirectToLogin();
					// return;
				}
			};

			getMe();

			setRenderCom(true);
		}, []);

		return (
			<div>
				{renderCom && <WrappedComponent {...props}>{children}</WrappedComponent>}
			</div>
		);
	};

	return FuncComponent;
};

export default authHoc;
