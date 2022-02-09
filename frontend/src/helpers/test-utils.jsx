/* eslint-disable react/prop-types */
import React from 'react';
import {render} from '@testing-library/react';
import NotificationProvider from '../components/NotificationProvider';
import store from '../redux/store';
import { Provider } from 'react-redux';
import '../i18n';

const AllTheProviders = ({children}) => {
	return (
		<Provider store={store}>
			<NotificationProvider>
				{children}
			</NotificationProvider>
		</Provider>
	);
};

const customRender = (ui, options) =>
	render(ui, {wrapper: AllTheProviders, ...options});

// re-export everything
export * from '@testing-library/react';

// override render method
export {customRender as render};

  