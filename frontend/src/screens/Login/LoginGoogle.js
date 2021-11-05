import React from 'react';
import { useGoogleLogin } from 'react-google-login';
import { IS_AUTH } from '../../constants/envVar';
import * as axiosHelper from '../../helpers/axiosHelper';
import { changeIsLogin } from '../../redux/actions/navbarAction';
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_IMG_URL} from '../../constants/envVar';
import { useDispatch } from 'react-redux';

// refresh token
// import { refreshTokenSetup } from './refreshToken';

// const clientId =
// 	'1006597644137-plgvccnt0d3keaojro5q3j69vkjudfvs.apps.googleusercontent.com';

function LoginHooks() {
	const dispatch = useDispatch();
	const onSuccess = async (res) => {
		const siginInResult = await axiosHelper.SignInWithGoogle({
			access_token: res.accessToken,
			platform: 'web'
		});
		alert(
			`Đăng nhập thành công chào mừng ${res.profileObj.name}.`
		);
		// refreshTokenSetup(res);
		sessionStorage.setItem(IS_AUTH, res);
		dispatch(changeIsLogin(true));
		localStorage.setItem(ACCESS_TOKEN, siginInResult.data.accessToken);
		localStorage.setItem(REFRESH_TOKEN, siginInResult.data.refreshToken);
		localStorage.setItem(USER_IMG_URL, res.profileObj.imageUrl);
		if (res.profileObj) {
			window.location.replace('/');
		}
	};

	// const onSuccess = async (res) => {
	// 	try {
	// 		setIsLoading(true);
	// 		const siginInResult = await axiosHelper.SignIn({
	// 			access_token: res.accessToken,
	// 			platform: 'web'
	// 		});
	// 		dispatch(changeIsLogin(true));
	// 		localStorage.setItem(ACCESS_TOKEN, siginInResult.data.accessToken);
	// 		localStorage.setItem(REFRESH_TOKEN, siginInResult.data.refreshToken);
	// 		localStorage.setItem(USER_IMG_URL, res.profileObj.imageUrl);
	// 		setIsLoading(false);
	// 	}catch (e) {
	// 		setIsLoading(false);
	// 		alert(e);
	// 	}
	// 	// refreshTokenSetup(res);
	// };

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