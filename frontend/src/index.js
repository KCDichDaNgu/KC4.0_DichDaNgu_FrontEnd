import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';
import './i18n';
import store from './redux/store';
import './custom.scss';
import NotificationProvider from './components/NotificationProvider';

ReactDOM.render(
	<React.StrictMode>
		<Provider store={store}>
			<NotificationProvider>
				<App />
			</NotificationProvider>
		</Provider>
	</React.StrictMode>,
	document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
