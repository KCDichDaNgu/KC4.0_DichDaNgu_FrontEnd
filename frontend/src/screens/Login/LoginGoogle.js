import React from 'react';
import { useGoogleLogin } from 'react-google-login';
import { IS_AUTH } from '../../constants/envVar';

// refresh token
// import { refreshTokenSetup } from './refreshToken';

// const clientId =
// 	'1006597644137-plgvccnt0d3keaojro5q3j69vkjudfvs.apps.googleusercontent.com';

function LoginHooks() {
	const onSuccess = (res) => {
		console.log('Login Success: currentUser:', res.accessToken);
		alert(
			`Đăng nhập thành công chào mừng ${res.profileObj.name}.`
		);
		// refreshTokenSetup(res);
		sessionStorage.setItem(IS_AUTH, res);
		if (res.profileObj) {
			window.location.replace('/');
		}
	};

	// eslint-disable-next-line no-unused-vars
	const onFailure = (res) => {
		alert(
			'Đăng nhập thất bại'
		);
	};

	const { signIn } = useGoogleLogin({
		onSuccess,
		onFailure,
		// eslint-disable-next-line no-undef
		clientId: process.env.REACT_APP_CLIENT_ID,
		isSignedIn: false,
		accessType: 'offline',
		// responseType: 'code',
		// prompt: 'consent',
	});

	return (
		<>
			<button onClick={() => signIn()} style={{ backgroundColor: '#EA4335', borderRadius: 10 }} className="btn btn-danger btn-block">
				<i className="fab fa-google fa-fw" /> Đăng nhập với Google
			</button>

		</>

	);
}

export default LoginHooks;